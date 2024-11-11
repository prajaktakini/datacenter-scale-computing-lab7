import json
import os
import requests
import redis
from minio import Minio
import platform
import sys

# Step 1: create redis client
redisHost = os.getenv("REDIS_HOST") or "localhost"
redisPort = os.getenv("REDIS_PORT") or "6379"
redisQueue = os.getenv("REDIS_QUEUE") or "toWorkers"

# Initialize redis client
redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0, decode_responses=True)

# Step 2: create minio client
# Minio is open-source "object-store" similar to Amazon S3
# API Reference: https://min.io/docs/minio/linux/developers/python/API.html
minioEndpoint = os.getenv("MINIO_ENDPOINT") or "localhost:9000"
minioAccessKey = os.getenv("MINIO_ACCESS_KEY") or "rootuser"
minioSecretKey = os.getenv("MINIO_SECRET_KEY") or "rootpass123"

# Initialize minio client
minioClient = Minio(minioEndpoint, access_key=minioAccessKey, secret_key=minioSecretKey, secure=False)

LOGGING_WORKER_QUEUE = os.getenv("LOGGING_WORKER_QUEUE") or "logging"
MINIO_BUCKET = "waveform-song-queue"
MINIO_SEPARATED_TRACK_BUCKET = "waveform-separation-track-queue"

infoKey = "{}.rest.info".format(platform.node())
debugKey = "{}.rest.debug".format(platform.node())
errorKey = "{}.rest.error".format(platform.node())

def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    redisClient.lpush(LOGGING_WORKER_QUEUE, f"{key}:{message}")

def log_info(message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    redisClient.lpush(LOGGING_WORKER_QUEUE, f"{key}:{message}")

def log_error(message, key=errorKey):
    print("ERROR:", message, file=sys.stdout)
    redisClient.lpush(LOGGING_WORKER_QUEUE, f"{key}:{message}")

def process_message(message):
    try:
        # Parse message data
        print("Raw message data:", message)
        data = json.loads(message)
        song_hash = data["song_hash"]
        callback_url = data["callback_url"]
        callback_data = data["callback_data"]["data"]
        print(f"Extracted song hash: {song_hash}")
        print(f"Extracted callback URL: {callback_url}")
        #print(f"processing song with hash {song_hash}")

        # Download song from Minio
        input_path = f"/data/input/{song_hash}.mp3"
        print(f"Attempting to download song from MinIO to path: {input_path}")

        minioClient.fget_object(MINIO_BUCKET, f"{song_hash}.mp3", input_path)
        print(f"Successfully downloaded song with hash {song_hash} from MinIO to {input_path}")
        log_info(f"Downloaded song with hash {song_hash} from Minio")

        # Separate tracks using DEMUCS software
        print(f"Starting DEMUCS separation for {input_path}")
        result = os.system(f"python3 -m demucs.separate --out /data/output --mp3 {input_path}")

        if result == 0:
            print(f"Track separation successful for song with hash {song_hash}")
            log_info(f"Completed track separation for song with hash {song_hash} using DEMUCS")
        else:
            print(f"Track separation failed for song with hash {song_hash}")
            log_info(f"Failed track separation for song with hash {song_hash}")

        for part in ["bass", "drums", "vocals", "other"]:
            track_path = f"/data/output/mdx_extra_q/{song_hash}/{part}.mp3"
            print(f"Attempting to upload {part}.mp3 for song with hash {song_hash} to MinIO")
            minioClient.fput_object(
                MINIO_SEPARATED_TRACK_BUCKET,
                f"{song_hash}_{part}.mp3",
                 track_path,
                content_type="audio/mpeg"
            )
            print(f"Uploaded {part}.mp3 for song with hash {song_hash} to MinIO")

        # Prepare callback payload
        callback_payload = {
            "song_hash": song_hash,
            "status": "SUCCESS",
            "tracks": {part: f"{song_hash}_{part}.mp3" for part in ["bass", "drums", "vocals", "other"]}
        }
        # Include additional data if specified
        if callback_data:
            callback_payload["callback_data"] = callback_data

        print(f"Prepared callback payload: {callback_payload}")

        # Send callback if URL is specified
        if callback_url:
            print(f"Sending callback to {callback_url}")
            response = requests.post(callback_url, json=callback_payload)
            print(f"Callback sent for song with hash {song_hash}, response status: {response.status_code}")
        else:
            print("No callback URL provided, skipping callback")
        # # Upload separated tracks to Minio object store
        # minioClient.fput_object(MINIO_SEPARATED_TRACK_BUCKET, f"bass_{songHash}.mp3", "/data/output/mdx_extra_q/" + str(songHash) + "/bass.mp3")
        # log_info(f"Uploaded bass.mp3 for song with hash {songHash} to Minio object store")
        # minioClient.fput_object(MINIO_SEPARATED_TRACK_BUCKET, f"bass_{songHash}.mp3", "/data/output/mdx_extra_q/" + str(songHash) + "/vocals.mp3")
        # log_info(f"Uploaded vocals.mp3 for song with hash {songHash} to Minio object store")
        # minioClient.fput_object(MINIO_SEPARATED_TRACK_BUCKET, f"bass_{songHash}.mp3", "/data/output/mdx_extra_q/" + str(songHash) + "/drums.mp3")
        # log_info(f"Uploaded drums.mp3 for song with hash {songHash} to Minio object store")
        # minioClient.fput_object(MINIO_SEPARATED_TRACK_BUCKET, f"bass_{songHash}.mp3", "/data/output/mdx_extra_q/" + str(songHash) + "/other.mp3")
        # log_info(f"Uploaded other.mp3 for song with hash {songHash} to Minio object store")
        #
        # # If callback is specified, handle it
        # if "callback_url" in data:
        #     payload = {
        #         "song_hash": songHash,
        #         "status": "SUCCESS",
        #         "tracks": [f"{songHash}/{part}.mp3" for part in ["bass", "drums", "vocals", "other"]]
        #     }
        #     requests.post(data["callback_url"], json=payload)
        #     log_info(f"Callback sent for song with hash {songHash} to Minio object store")

    except Exception as ex:
        print("Worker Received exception:", ex)
        log_error(f"Error, received exception {ex}", errorKey)

def main():
    log_info("Redis worker started, listening for messages containing mp3 track.....")
    print("DEBUG: Redis worker has started...")
    while True:
        print("DEBUG: Waiting for messages on Redis queue...")
        # Start blocking call that waits for messages from redis queue
        message = redisClient.blpop(redisQueue, timeout=0) # returns tuple
        if message:
            print("DEBUG: Message received from Redis:", message)
            _, data = message
            print("DEBUG: Calling process_message with data:", data)
            process_message(data)


if __name__ == "__main__":
    main()


