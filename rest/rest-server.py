import hashlib
import os
import io
from flask import Flask, request, Response, jsonify
import base64
import redis
import json
from minio import Minio
import requests
import platform
import sys
import logging


# Step 1: create redis client
redisHost = os.getenv("REDIS_HOST") or "localhost"
redisPort = os.getenv("REDIS_PORT") or 6379

# Initialize redis client
redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)

# Step 2: Flask server
flaskHost = os.getenv("FLASK_HOST") or "localhost"
flaskPort = os.getenv("FLASK_PORT") or 5000

app = Flask(__name__)

# Step 3: create minio client
# Minio is open-source "object-store" similar to Amazon S3
# API Reference: https://min.io/docs/minio/linux/developers/python/API.html
minioEndpoint = os.getenv("MINIO_ENDPOINT") or "localhost:9000"
minioAccessKey = os.getenv("MINIO_ACCESS_KEY") or "rootuser"
minioSecretKey = os.getenv("MINIO_SECRET_KEY") or "rootpass123"

# Initialize minio client
minioClient = Minio(minioEndpoint, access_key=minioAccessKey, secret_key=minioSecretKey, secure=False)
MINIO_BUCKET = "waveform-song-queue"
MINIO_SEPARATED_TRACK_BUCKET = "waveform-separation-track-queue"
redisQueue = os.getenv("REDIS_QUEUE") or "toWorkers"

LOGGING_WORKER_QUEUE = os.getenv("LOGGING_WORKER_QUEUE") or "logging"

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

# Create buckets 1. to store mp3 2. to store separated tracks
for bucket in [MINIO_BUCKET, MINIO_SEPARATED_TRACK_BUCKET]:
    if not minioClient.bucket_exists(bucket):
        print(f"Creating bucket: {bucket}")
        minioClient.make_bucket(bucket)


@app.route('/apiv1/separate', methods=['POST'])
def separate():
    try:
        log_info("Received request to separate music mp3", infoKey)
        data = json.loads(request.get_data())
        mp3_base64 = data['mp3']
        callback = data['callback']

        # Decode MP3 data from base64
        mp3 = base64.b64decode(mp3_base64)
        mp3_length = len(mp3)

        # Generate a unique hash for the file
        mp3_hash = hashlib.sha256(mp3).hexdigest()

        # Create a message containing the hash and callback
        message = {
            "song_hash": mp3_hash,
            "callback_url": callback['url'],
            "callback_data": callback['data']
        }

        # Add the hash to Redis queue
        redisClient.rpush(redisQueue, json.dumps(message))

        # Store MP3 in Minio
        minioClient.put_object(MINIO_BUCKET, f"{mp3_hash}.mp3", io.BytesIO(mp3), mp3_length, content_type="audio/mpeg")

        # Respond with the unique identifier
        response = {'hash': mp3_hash, 'message': 'Song enqueued for separation'}
        return Response(json.dumps(response), status=200, mimetype="application/json")

    except Exception as err:
        log_error(f"Error, received exception {err}", errorKey)
        # Return an error response with details
        error_response = {'message': 'Error occurred', 'details': str(err)}
        return Response(json.dumps(error_response), status=500, mimetype="application/json")


@app.route('/callback', methods=['POST'])
def handle_callback():
    try:
        # Parse incoming callback data
        data = request.get_json()
        print("Received callback data:", data)
        log_info(f"Received callback data: {data}", infoKey)
        song_hash = data['song_hash']
        status = data['status']
        tracks = data['tracks']

        # Print the tracks received in the callback payload
        print(f"Received callback for song hash: {song_hash}")
        print(f"Status: {status}")
        print("Tracks received:")
        log_info(f"Received callback for song hash: {song_hash}", infoKey)

        # Print each track's name and its corresponding URL or path
        for part, track_url in tracks.items():
            print(f"{part.capitalize()} track: {track_url}")

        log_info(f"Processed callback successfully: {song_hash}", infoKey)
        return jsonify({"message": "Callback received successfully."}), 200

    except Exception as ex:
        # Handle any errors that occur while processing the callback
        print(f"Error processing callback: {str(ex)}")
        log_error(f"Error processing callback: {str(ex)}", errorKey)
        return jsonify({"message": "Error processing callback."}), 500


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
app.logger.setLevel(logging.DEBUG)

@app.route('/apiv1/queue', methods=['GET'])
def get_queue():
    try:
        # Retrieve all items from the Redis queue
        log_info("Received request to fetch queued items from Redis", infoKey)
        queue_items = redisClient.lrange(redisQueue, 0, -1)
        # Decode each item for readability
        queue_data = [json.loads(item) for item in queue_items]
        log_info(f"Fetched {len(queue_data)} items from the queue", infoKey)

        # Return the queue data as JSON
        return jsonify({"queue": queue_data}), 200

    except Exception as err:
        log_error(f"Error retrieving queue: {err}", errorKey)
        return jsonify({"message": "Error occurred", "details": str(err)}), 500


@app.route('/apiv1/track/<song_hash>/<track>', methods=['GET'])
def get_track(song_hash, track):
    try:
        track_file = f"{song_hash}_{track}.mp3"
        app.logger.debug(f"Attempting to retrieve track: {track_file} from MinIO")
        log_info(f"Attempting to retrieve track: {track_file} from MinIO", infoKey)

        # Simulate fetching track from MinIO (replace this with actual minioClient logic)
        response = minioClient.get_object(MINIO_SEPARATED_TRACK_BUCKET, track_file)

        app.logger.debug(f"Successfully retrieved the track: {track_file} from MinIO")
        log_info(f"Successfully retrieved the track: {track_file} from MinIO", infoKey)

        content_length = len(response.data)
        app.logger.debug(f"Content length of the track: {content_length} bytes")
        log_info(f"Content length of the track: {content_length} bytes", infoKey)

        if content_length == 0:
            app.logger.error(f"Track {track_file} is empty (0 bytes)")
            log_info(f"Track {track_file} is empty (0 bytes)", infoKey)
            return jsonify({"message": "Track is empty", "details": f"{track_file} is 0 bytes."}), 400

        return Response(
            response.data,
            status=200,
            mimetype="audio/mpeg",
            headers={"Content-Disposition": f"attachment; filename={track_file}"}
        )
    except Exception as e:
        app.logger.error(f"Error retrieving track {track_file}: {e}")
        log_error(f"Error retrieving track {track_file}: {e}", errorKey)
        return jsonify({"message": "Error retrieving track", "details": str(e)}), 500


@app.route('/apiv1/remove/<song_hash>/<track>', methods=['DELETE'])
def delete_track(song_hash, track):
    try:
        # Delete the specific track from MinIO
        track_file = f"{song_hash}_{track}.mp3"
        log_info(f"Attempting to remove track: {track_file} from MinIO", infoKey)
        minioClient.remove_object(MINIO_SEPARATED_TRACK_BUCKET, track_file)
        log_info(f"Successfully removed the track: {track_file} from MinIO", infoKey)
        return jsonify({"message": f"Track {track_file} deleted successfully."}), 200
    except Exception as e:
        print(f"Error deleting track {track_file}: {e}")
        log_error(f"Error retrieving track {track_file}: {e}", errorKey)
        return jsonify({"message": "Error deleting track", "details": str(e)}), 500


if __name__ == "__main__":
    # Step 3: Run the Flask server
    app.run(host=flaskHost, port=flaskPort)