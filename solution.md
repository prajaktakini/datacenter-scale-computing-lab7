## Deployments
```
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ kubectl get pods
NAME                      READY   STATUS        RESTARTS   AGE
logs-d55d75fd7-mjvjv      1/1     Running       0          17h
redis-688ff754cd-86bcm    1/1     Running       0          19h
rest-f8ffcbd96-wsdnp      1/1     Running       0          40s
worker-67995d45fd-bvcpp   1/1     Running       0          26s
worker-67995d45fd-h9cnt   1/1     Terminating   0          7m45s
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ kubectl get pods -n minio-dev
NAME    READY   STATUS    RESTARTS   AGE
minio   1/1     Running   0          6h38m
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ kubectl get pods             
NAME                      READY   STATUS    RESTARTS   AGE
logs-d55d75fd7-mjvjv      1/1     Running   0          17h
redis-688ff754cd-86bcm    1/1     Running   0          19h
rest-f8ffcbd96-wsdnp      1/1     Running   0          53s
worker-67995d45fd-bvcpp   1/1     Running   0          39s
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ 
```
## Enable REST port forwarding
```
kubectl port-forward --address 0.0.0.0 service/rest 5001:5000
```

## Enable Minio port forwarding
```
kubectl port-forward -n minio-dev --address 0.0.0.0 service/minio 9090:9090
```
## API calls
```
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ python3 short-sample-request.py 
Separate data/data/short-hop.mp3
Response to http://localhost:5001/apiv1/separate request is <class 'dict'>
Make request http://localhost:5001/apiv1/separate with json dict_keys(['mp3', 'callback'])
mp3 is of type <class 'str'> and length 347248 
Success response
{
    "hash": "9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28",
    "message": "Song enqueued for separation"
}
Cache from server is
Separate data/data/short-dreams.mp3
Response to http://localhost:5001/apiv1/separate request is <class 'dict'>
Make request http://localhost:5001/apiv1/separate with json dict_keys(['mp3', 'callback'])
mp3 is of type <class 'str'> and length 210212 
Success response
{
    "hash": "83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666",
    "message": "Song enqueued for separation"
}
Cache from server is
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ curl -X GET http://localhost:5001/apiv1/queue
{"queue":[]}
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ curl -X GET "http://localhost:5001/apiv1/track/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666/vocals" -o vocals.mp3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  279k  100  279k    0     0  1798k      0 --:--:-- --:--:-- --:--:-- 1803k
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ curl -X GET "http://localhost:5001/apiv1/track/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666/bass" -o bass.mp3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  279k  100  279k    0     0   996k      0 --:--:-- --:--:-- --:--:--  998k
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ curl -X GET "http://localhost:5001/apiv1/track/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666/drums" -o drums.mp3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  279k  100  279k    0     0  2858k      0 --:--:-- --:--:-- --:--:-- 2852k
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ curl -X GET "http://localhost:5001/apiv1/track/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666/other" -o other.mp3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  279k  100  279k    0     0  4765k      0 --:--:-- --:--:-- --:--:-- 4820k
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ curl -x DELETE "http://localhost:5001/apiv1/track/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666/vocals"
curl: (5) Could not resolve proxy: DELETE
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ curl -x DELETE "http://localhost:5001/apiv1/remove/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666/vocals"
curl: (5) Could not resolve proxy: DELETE
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ curl -X DELETE "http://localhost:5001/apiv1/remove/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666/vocals"
{"message":"Track 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666_vocals.mp3 deleted successfully."}
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ curl -X DELETE "http://localhost:5001/apiv1/remove/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666/vocals"
{"message":"Track 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666_vocals.mp3 deleted successfully."}
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ python3 short-sample-request.py                                                                                                      
Separate data/data/short-hop.mp3
Response to http://localhost:5001/apiv1/separate request is <class 'dict'>
Make request http://localhost:5001/apiv1/separate with json dict_keys(['mp3', 'callback'])
mp3 is of type <class 'str'> and length 347248 
Success response
{
    "hash": "9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28",
    "message": "Song enqueued for separation"
}
Cache from server is
Separate data/data/short-dreams.mp3
Response to http://localhost:5001/apiv1/separate request is <class 'dict'>
Make request http://localhost:5001/apiv1/separate with json dict_keys(['mp3', 'callback'])
mp3 is of type <class 'str'> and length 210212 
Success response
{
    "hash": "83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666",
    "message": "Song enqueued for separation"
}
Cache from server is
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ curl -X GET http://localhost:5001/apiv1/queue
{"queue":[{"callback_data":{"data":"to be returned","mp3":"data/short-dreams.mp3"},"callback_url":"http://rest:5000/callback","song_hash":"83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666"}]}
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ 
```

## Logs of logs docker container
```
rest-f8ffcbd96-wsdnp.rest.info:Received request to separate music mp3
rest-f8ffcbd96-wsdnp.rest.info:Received request to separate music mp3
worker-67995d45fd-bvcpp.rest.info:Downloaded song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 from Minio
worker-67995d45fd-bvcpp.rest.info:Completed track separation for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 using DEMUCS
rest-f8ffcbd96-wsdnp.rest.info:Received callback data: {'song_hash': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28', 'status': 'SUCCESS', 'tracks': {'bass': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_bass.mp3', 'drums': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_drums.mp3', 'vocals': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_vocals.mp3', 'other': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_other.mp3'}, 'callback_data': 'to be returned'}
rest-f8ffcbd96-wsdnp.rest.info:Received callback for song hash: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
rest-f8ffcbd96-wsdnp.rest.info:Processed callback successfully: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
worker-67995d45fd-bvcpp.rest.info:Downloaded song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 from Minio
worker-67995d45fd-bvcpp.rest.info:Completed track separation for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 using DEMUCS
rest-f8ffcbd96-wsdnp.rest.info:Received callback data: {'song_hash': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666', 'status': 'SUCCESS', 'tracks': {'bass': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3', 'drums': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3', 'vocals': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3', 'other': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3'}, 'callback_data': 'to be returned'}
rest-f8ffcbd96-wsdnp.rest.info:Received callback for song hash: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666
rest-f8ffcbd96-wsdnp.rest.info:Processed callback successfully: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666
rest-f8ffcbd96-wsdnp.rest.info:Received request to fetch queued items from Redis
rest-f8ffcbd96-wsdnp.rest.info:Fetched 0 items from the queue
rest-f8ffcbd96-wsdnp.rest.info:Attempting to retrieve track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3 from MinIO
rest-f8ffcbd96-wsdnp.rest.info:Successfully retrieved the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3 from MinIO
rest-f8ffcbd96-wsdnp.rest.info:Content length of the track: 286302 bytes
rest-f8ffcbd96-wsdnp.rest.info:Attempting to retrieve track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3 from MinIO
rest-f8ffcbd96-wsdnp.rest.info:Successfully retrieved the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3 from MinIO
rest-f8ffcbd96-wsdnp.rest.info:Content length of the track: 286302 bytes
rest-f8ffcbd96-wsdnp.rest.info:Attempting to retrieve track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3 from MinIO
rest-f8ffcbd96-wsdnp.rest.info:Successfully retrieved the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3 from MinIO
rest-f8ffcbd96-wsdnp.rest.info:Content length of the track: 286302 bytes
rest-f8ffcbd96-wsdnp.rest.info:Attempting to retrieve track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3 from MinIO
rest-f8ffcbd96-wsdnp.rest.info:Successfully retrieved the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3 from MinIO
rest-f8ffcbd96-wsdnp.rest.info:Content length of the track: 286302 bytes
rest-f8ffcbd96-wsdnp.rest.info:Attempting to remove track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666_vocals.mp3 from MinIO
rest-f8ffcbd96-wsdnp.rest.info:Successfully removed the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666_vocals.mp3 from MinIO
rest-f8ffcbd96-wsdnp.rest.info:Attempting to remove track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666_vocals.mp3 from MinIO
rest-f8ffcbd96-wsdnp.rest.info:Successfully removed the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666_vocals.mp3 from MinIO
rest-f8ffcbd96-wsdnp.rest.info:Received request to separate music mp3
rest-f8ffcbd96-wsdnp.rest.info:Received request to separate music mp3
worker-67995d45fd-bvcpp.rest.info:Downloaded song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 from Minio
rest-f8ffcbd96-wsdnp.rest.info:Received request to fetch queued items from Redis
rest-f8ffcbd96-wsdnp.rest.info:Fetched 1 items from the queue
worker-67995d45fd-bvcpp.rest.info:Completed track separation for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 using DEMUCS
rest-f8ffcbd96-wsdnp.rest.info:Received callback data: {'song_hash': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28', 'status': 'SUCCESS', 'tracks': {'bass': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_bass.mp3', 'drums': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_drums.mp3', 'vocals': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_vocals.mp3', 'other': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_other.mp3'}, 'callback_data': 'to be returned'}
rest-f8ffcbd96-wsdnp.rest.info:Received callback for song hash: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
rest-f8ffcbd96-wsdnp.rest.info:Processed callback successfully: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
worker-67995d45fd-bvcpp.rest.info:Downloaded song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 from Minio
worker-67995d45fd-bvcpp.rest.info:Completed track separation for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 using DEMUCS
rest-f8ffcbd96-wsdnp.rest.info:Received callback data: {'song_hash': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666', 'status': 'SUCCESS', 'tracks': {'bass': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3', 'drums': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3', 'vocals': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3', 'other': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3'}, 'callback_data': 'to be returned'}
rest-f8ffcbd96-wsdnp.rest.info:Received callback for song hash: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666
rest-f8ffcbd96-wsdnp.rest.info:Processed callback successfully: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666

```

## Logs of flask server
```
2024-11-12 05:26:38,226 - INFO - WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://10.1.0.142:5000
2024-11-12 05:26:38,229 - INFO - Press CTRL+C to quit
INFO: Received request to separate music mp3
2024-11-12 05:29:45,711 - DEBUG - Resetting dropped connection: minio.minio-dev.svc.cluster.local
2024-11-12 05:29:45,815 - DEBUG - http://minio.minio-dev.svc.cluster.local:9000 "PUT /waveform-song-queue/9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28.mp3 HTTP/11" 200 0
2024-11-12 05:29:45,832 - INFO - 127.0.0.1 - - [12/Nov/2024 05:29:45] "POST /apiv1/separate HTTP/1.1" 200 -
INFO: Received request to separate music mp3
2024-11-12 05:29:45,907 - DEBUG - http://minio.minio-dev.svc.cluster.local:9000 "PUT /waveform-song-queue/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666.mp3 HTTP/11" 200 0
2024-11-12 05:29:45,908 - INFO - 127.0.0.1 - - [12/Nov/2024 05:29:45] "POST /apiv1/separate HTTP/1.1" 200 -
Received callback data: {'song_hash': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28', 'status': 'SUCCESS', 'tracks': {'bass': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_bass.mp3', 'drums': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_drums.mp3', 'vocals': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_vocals.mp3', 'other': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_other.mp3'}, 'callback_data': 'to be returned'}
INFO: Received callback data: {'song_hash': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28', 'status': 'SUCCESS', 'tracks': {'bass': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_bass.mp3', 'drums': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_drums.mp3', 'vocals': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_vocals.mp3', 'other': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_other.mp3'}, 'callback_data': 'to be returned'}
Received callback for song hash: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
Status: SUCCESS
Tracks received:
INFO: Received callback for song hash: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
Bass track: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_bass.mp3
Drums track: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_drums.mp3
Vocals track: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_vocals.mp3
Other track: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_other.mp3
INFO: Processed callback successfully: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
2024-11-12 05:30:57,895 - INFO - 10.1.0.143 - - [12/Nov/2024 05:30:57] "POST /callback HTTP/1.1" 200 -
Received callback data: {'song_hash': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666', 'status': 'SUCCESS', 'tracks': {'bass': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3', 'drums': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3', 'vocals': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3', 'other': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3'}, 'callback_data': 'to be returned'}
INFO: Received callback data: {'song_hash': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666', 'status': 'SUCCESS', 'tracks': {'bass': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3', 'drums': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3', 'vocals': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3', 'other': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3'}, 'callback_data': 'to be returned'}
Received callback for song hash: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666
Status: SUCCESS
Tracks received:
INFO: Received callback for song hash: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666
Bass track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3
Drums track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3
Vocals track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3
Other track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3
INFO: Processed callback successfully: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666
2024-11-12 05:31:35,770 - INFO - 10.1.0.143 - - [12/Nov/2024 05:31:35] "POST /callback HTTP/1.1" 200 -
INFO: Received request to fetch queued items from Redis
INFO: Fetched 0 items from the queue
2024-11-12 05:32:54,515 - INFO - 127.0.0.1 - - [12/Nov/2024 05:32:54] "GET /apiv1/queue HTTP/1.1" 200 -
2024-11-12 05:34:17,847 - DEBUG - Attempting to retrieve track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3 from MinIO
INFO: Attempting to retrieve track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3 from MinIO
2024-11-12 05:34:17,884 - DEBUG - Resetting dropped connection: minio.minio-dev.svc.cluster.local
2024-11-12 05:34:17,941 - DEBUG - http://minio.minio-dev.svc.cluster.local:9000 "GET /waveform-separation-track-queue/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3 HTTP/11" 200 286302
2024-11-12 05:34:17,941 - DEBUG - Successfully retrieved the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3 from MinIO
INFO: Successfully retrieved the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3 from MinIO
2024-11-12 05:34:17,955 - DEBUG - Content length of the track: 286302 bytes
INFO: Content length of the track: 286302 bytes
2024-11-12 05:34:17,958 - INFO - 127.0.0.1 - - [12/Nov/2024 05:34:17] "GET /apiv1/track/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666/vocals HTTP/1.1" 200 -
2024-11-12 05:34:48,210 - DEBUG - Attempting to retrieve track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3 from MinIO
INFO: Attempting to retrieve track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3 from MinIO
2024-11-12 05:34:48,260 - DEBUG - Resetting dropped connection: minio.minio-dev.svc.cluster.local
2024-11-12 05:34:48,357 - DEBUG - http://minio.minio-dev.svc.cluster.local:9000 "GET /waveform-separation-track-queue/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3 HTTP/11" 200 286302
INFO: Successfully retrieved the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3 from MinIO
2024-11-12 05:34:48,358 - DEBUG - Successfully retrieved the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3 from MinIO
2024-11-12 05:34:48,374 - DEBUG - Content length of the track: 286302 bytes
INFO: Content length of the track: 286302 bytes
2024-11-12 05:34:48,378 - INFO - 127.0.0.1 - - [12/Nov/2024 05:34:48] "GET /apiv1/track/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666/bass HTTP/1.1" 200 -
2024-11-12 05:35:12,637 - DEBUG - Attempting to retrieve track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3 from MinIO
INFO: Attempting to retrieve track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3 from MinIO
2024-11-12 05:35:12,691 - DEBUG - http://minio.minio-dev.svc.cluster.local:9000 "GET /waveform-separation-track-queue/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3 HTTP/11" 200 286302
INFO: Successfully retrieved the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3 from MinIO
2024-11-12 05:35:12,692 - DEBUG - Successfully retrieved the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3 from MinIO
INFO: Content length of the track: 286302 bytes
2024-11-12 05:35:12,694 - DEBUG - Content length of the track: 286302 bytes
2024-11-12 05:35:12,697 - INFO - 127.0.0.1 - - [12/Nov/2024 05:35:12] "GET /apiv1/track/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666/drums HTTP/1.1" 200 -
INFO: Attempting to retrieve track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3 from MinIO
2024-11-12 05:35:37,083 - DEBUG - Attempting to retrieve track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3 from MinIO
2024-11-12 05:35:37,100 - DEBUG - http://minio.minio-dev.svc.cluster.local:9000 "GET /waveform-separation-track-queue/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3 HTTP/11" 200 286302
INFO: Successfully retrieved the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3 from MinIO
2024-11-12 05:35:37,100 - DEBUG - Successfully retrieved the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3 from MinIO
2024-11-12 05:35:37,104 - DEBUG - Content length of the track: 286302 bytes
INFO: Content length of the track: 286302 bytes
2024-11-12 05:35:37,106 - INFO - 127.0.0.1 - - [12/Nov/2024 05:35:37] "GET /apiv1/track/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666/other HTTP/1.1" 200 -
INFO: Attempting to remove track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666_vocals.mp3 from MinIO
2024-11-12 05:37:29,695 - DEBUG - Resetting dropped connection: minio.minio-dev.svc.cluster.local
2024-11-12 05:37:29,732 - DEBUG - http://minio.minio-dev.svc.cluster.local:9000 "DELETE /waveform-separation-track-queue/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666_vocals.mp3 HTTP/11" 204 0
INFO: Successfully removed the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666_vocals.mp3 from MinIO
2024-11-12 05:37:29,737 - INFO - 127.0.0.1 - - [12/Nov/2024 05:37:29] "DELETE /apiv1/remove/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666/vocals HTTP/1.1" 200 -
INFO: Attempting to remove track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666_vocals.mp3 from MinIO
2024-11-12 05:39:40,166 - DEBUG - Resetting dropped connection: minio.minio-dev.svc.cluster.local
2024-11-12 05:39:40,232 - DEBUG - http://minio.minio-dev.svc.cluster.local:9000 "DELETE /waveform-separation-track-queue/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666_vocals.mp3 HTTP/11" 204 0
INFO: Successfully removed the track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666_vocals.mp3 from MinIO
2024-11-12 05:39:40,239 - INFO - 127.0.0.1 - - [12/Nov/2024 05:39:40] "DELETE /apiv1/remove/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2aa666/vocals HTTP/1.1" 200 -
INFO: Received request to separate music mp3
2024-11-12 05:42:24,843 - DEBUG - Resetting dropped connection: minio.minio-dev.svc.cluster.local
2024-11-12 05:42:24,949 - DEBUG - http://minio.minio-dev.svc.cluster.local:9000 "PUT /waveform-song-queue/9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28.mp3 HTTP/11" 200 0
2024-11-12 05:42:24,957 - INFO - 127.0.0.1 - - [12/Nov/2024 05:42:24] "POST /apiv1/separate HTTP/1.1" 200 -
INFO: Received request to separate music mp3
2024-11-12 05:42:25,045 - DEBUG - http://minio.minio-dev.svc.cluster.local:9000 "PUT /waveform-song-queue/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666.mp3 HTTP/11" 200 0
2024-11-12 05:42:25,046 - INFO - 127.0.0.1 - - [12/Nov/2024 05:42:25] "POST /apiv1/separate HTTP/1.1" 200 -
INFO: Received request to fetch queued items from Redis
INFO: Fetched 1 items from the queue
2024-11-12 05:42:38,812 - INFO - 127.0.0.1 - - [12/Nov/2024 05:42:38] "GET /apiv1/queue HTTP/1.1" 200 -
Received callback data: {'song_hash': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28', 'status': 'SUCCESS', 'tracks': {'bass': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_bass.mp3', 'drums': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_drums.mp3', 'vocals': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_vocals.mp3', 'other': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_other.mp3'}, 'callback_data': 'to be returned'}
INFO: Received callback data: {'song_hash': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28', 'status': 'SUCCESS', 'tracks': {'bass': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_bass.mp3', 'drums': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_drums.mp3', 'vocals': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_vocals.mp3', 'other': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_other.mp3'}, 'callback_data': 'to be returned'}
Received callback for song hash: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
Status: SUCCESS
Tracks received:
INFO: Received callback for song hash: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
Bass track: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_bass.mp3
Drums track: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_drums.mp3
Vocals track: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_vocals.mp3
Other track: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_other.mp3
INFO: Processed callback successfully: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
2024-11-12 05:43:52,294 - INFO - 10.1.0.143 - - [12/Nov/2024 05:43:52] "POST /callback HTTP/1.1" 200 -
Received callback data: {'song_hash': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666', 'status': 'SUCCESS', 'tracks': {'bass': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3', 'drums': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3', 'vocals': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3', 'other': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3'}, 'callback_data': 'to be returned'}
INFO: Received callback data: {'song_hash': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666', 'status': 'SUCCESS', 'tracks': {'bass': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3', 'drums': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3', 'vocals': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3', 'other': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3'}, 'callback_data': 'to be returned'}
Received callback for song hash: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666
Status: SUCCESS
Tracks received:
INFO: Received callback for song hash: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666
Bass track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3
Drums track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3
Vocals track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3
Other track: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3
INFO: Processed callback successfully: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666
2024-11-12 05:45:07,674 - INFO - 10.1.0.143 - - [12/Nov/2024 05:45:07] "POST /callback HTTP/1.1" 200 -

```

## Logs of Worker service
```
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ kubectl logs -f worker-67995d45fd-bvcpp 
INFO: Redis worker started, listening for messages containing mp3 track.....
DEBUG: Redis worker has started...
DEBUG: Waiting for messages on Redis queue...
DEBUG: Message received from Redis: ('toWorkers', '{"song_hash": "9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28", "callback_url": "http://rest:5000/callback", "callback_data": {"mp3": "data/short-hop.mp3", "data": "to be returned"}}')
DEBUG: Calling process_message with data: {"song_hash": "9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28", "callback_url": "http://rest:5000/callback", "callback_data": {"mp3": "data/short-hop.mp3", "data": "to be returned"}}
Raw message data: {"song_hash": "9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28", "callback_url": "http://rest:5000/callback", "callback_data": {"mp3": "data/short-hop.mp3", "data": "to be returned"}}
Extracted song hash: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
Extracted callback URL: http://rest:5000/callback
Attempting to download song from MinIO to path: /data/input/9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28.mp3
Successfully downloaded song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 from MinIO to /data/input/9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28.mp3
INFO: Downloaded song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 from Minio
Starting DEMUCS separation for /data/input/9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28.mp3
Selected model is a bag of 4 models. You will see that many progress bars per track.
Separated tracks will be stored in /data/output/mdx_extra_q
Separating track /data/input/9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28.mp3
  0%|                                                                                   | 0.0/33.0 [00:00<?, ?seconds/s][W NNPACK.cpp:79] Could not initialize NNPACK! Reason: Unsupported hardware.
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:13<00:00,  2.44seconds/s]
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:10<00:00,  3.10seconds/s]
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:08<00:00,  3.82seconds/s]
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:10<00:00,  3.07seconds/s]
Track separation successful for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
INFO: Completed track separation for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 using DEMUCS
Attempting to upload bass.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Uploaded bass.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Attempting to upload drums.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Uploaded drums.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Attempting to upload vocals.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Uploaded vocals.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Attempting to upload other.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Uploaded other.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Prepared callback payload: {'song_hash': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28', 'status': 'SUCCESS', 'tracks': {'bass': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_bass.mp3', 'drums': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_drums.mp3', 'vocals': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_vocals.mp3', 'other': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_other.mp3'}, 'callback_data': 'to be returned'}
Sending callback to http://rest:5000/callback
Callback sent for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28, response status: 200
DEBUG: Waiting for messages on Redis queue...
DEBUG: Message received from Redis: ('toWorkers', '{"song_hash": "83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666", "callback_url": "http://rest:5000/callback", "callback_data": {"mp3": "data/short-dreams.mp3", "data": "to be returned"}}')
DEBUG: Calling process_message with data: {"song_hash": "83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666", "callback_url": "http://rest:5000/callback", "callback_data": {"mp3": "data/short-dreams.mp3", "data": "to be returned"}}
Raw message data: {"song_hash": "83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666", "callback_url": "http://rest:5000/callback", "callback_data": {"mp3": "data/short-dreams.mp3", "data": "to be returned"}}
Extracted song hash: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666
Extracted callback URL: http://rest:5000/callback
Attempting to download song from MinIO to path: /data/input/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666.mp3
Successfully downloaded song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 from MinIO to /data/input/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666.mp3
INFO: Downloaded song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 from Minio
Starting DEMUCS separation for /data/input/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666.mp3
Selected model is a bag of 4 models. You will see that many progress bars per track.
Separated tracks will be stored in /data/output/mdx_extra_q
Separating track /data/input/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666.mp3
  0%|                                                                                   | 0.0/33.0 [00:00<?, ?seconds/s][W NNPACK.cpp:79] Could not initialize NNPACK! Reason: Unsupported hardware.
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:05<00:00,  5.52seconds/s]
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:06<00:00,  5.32seconds/s]
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:05<00:00,  5.56seconds/s]
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:05<00:00,  5.93seconds/s]
Track separation successful for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666
INFO: Completed track separation for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 using DEMUCS
Attempting to upload bass.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Uploaded bass.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Attempting to upload drums.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Uploaded drums.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Attempting to upload vocals.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Uploaded vocals.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Attempting to upload other.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Uploaded other.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Prepared callback payload: {'song_hash': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666', 'status': 'SUCCESS', 'tracks': {'bass': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3', 'drums': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3', 'vocals': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3', 'other': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3'}, 'callback_data': 'to be returned'}
Sending callback to http://rest:5000/callback
Callback sent for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666, response status: 200
DEBUG: Waiting for messages on Redis queue...
DEBUG: Message received from Redis: ('toWorkers', '{"song_hash": "9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28", "callback_url": "http://rest:5000/callback", "callback_data": {"mp3": "data/short-hop.mp3", "data": "to be returned"}}')
DEBUG: Calling process_message with data: {"song_hash": "9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28", "callback_url": "http://rest:5000/callback", "callback_data": {"mp3": "data/short-hop.mp3", "data": "to be returned"}}
Raw message data: {"song_hash": "9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28", "callback_url": "http://rest:5000/callback", "callback_data": {"mp3": "data/short-hop.mp3", "data": "to be returned"}}
Extracted song hash: 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
Extracted callback URL: http://rest:5000/callback
Attempting to download song from MinIO to path: /data/input/9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28.mp3
Successfully downloaded song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 from MinIO to /data/input/9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28.mp3
INFO: Downloaded song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 from Minio
Starting DEMUCS separation for /data/input/9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28.mp3
Selected model is a bag of 4 models. You will see that many progress bars per track.
Separated tracks will be stored in /data/output/mdx_extra_q
Separating track /data/input/9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28.mp3
  0%|                                                                                   | 0.0/33.0 [00:00<?, ?seconds/s][W NNPACK.cpp:79] Could not initialize NNPACK! Reason: Unsupported hardware.
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:16<00:00,  2.02seconds/s]
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:12<00:00,  2.74seconds/s]
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:11<00:00,  2.96seconds/s]
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:19<00:00,  1.66seconds/s]
Track separation successful for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28
INFO: Completed track separation for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 using DEMUCS
Attempting to upload bass.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Uploaded bass.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Attempting to upload drums.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Uploaded drums.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Attempting to upload vocals.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Uploaded vocals.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Attempting to upload other.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Uploaded other.mp3 for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28 to MinIO
Prepared callback payload: {'song_hash': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28', 'status': 'SUCCESS', 'tracks': {'bass': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_bass.mp3', 'drums': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_drums.mp3', 'vocals': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_vocals.mp3', 'other': '9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28_other.mp3'}, 'callback_data': 'to be returned'}
Sending callback to http://rest:5000/callback
Callback sent for song with hash 9627ed8f6b9ddd5b86fa495161a6de2ab371e2ed8e052d659a88c51272b4fc28, response status: 200
DEBUG: Waiting for messages on Redis queue...
DEBUG: Message received from Redis: ('toWorkers', '{"song_hash": "83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666", "callback_url": "http://rest:5000/callback", "callback_data": {"mp3": "data/short-dreams.mp3", "data": "to be returned"}}')
DEBUG: Calling process_message with data: {"song_hash": "83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666", "callback_url": "http://rest:5000/callback", "callback_data": {"mp3": "data/short-dreams.mp3", "data": "to be returned"}}
Raw message data: {"song_hash": "83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666", "callback_url": "http://rest:5000/callback", "callback_data": {"mp3": "data/short-dreams.mp3", "data": "to be returned"}}
Extracted song hash: 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666
Extracted callback URL: http://rest:5000/callback
Attempting to download song from MinIO to path: /data/input/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666.mp3
Successfully downloaded song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 from MinIO to /data/input/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666.mp3
INFO: Downloaded song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 from Minio
Starting DEMUCS separation for /data/input/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666.mp3
Selected model is a bag of 4 models. You will see that many progress bars per track.
Separated tracks will be stored in /data/output/mdx_extra_q
Separating track /data/input/83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666.mp3
  0%|                                                                                   | 0.0/33.0 [00:00<?, ?seconds/s][W NNPACK.cpp:79] Could not initialize NNPACK! Reason: Unsupported hardware.
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:10<00:00,  3.19seconds/s]
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:05<00:00,  5.53seconds/s]
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:17<00:00,  1.84seconds/s]
100%|██████████████████████████████████████████████████████████████████████████| 33.0/33.0 [00:08<00:00,  4.03seconds/s]
Track separation successful for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666
INFO: Completed track separation for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 using DEMUCS
Attempting to upload bass.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Uploaded bass.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Attempting to upload drums.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Uploaded drums.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Attempting to upload vocals.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Uploaded vocals.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Attempting to upload other.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Uploaded other.mp3 for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666 to MinIO
Prepared callback payload: {'song_hash': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666', 'status': 'SUCCESS', 'tracks': {'bass': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_bass.mp3', 'drums': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_drums.mp3', 'vocals': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_vocals.mp3', 'other': '83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666_other.mp3'}, 'callback_data': 'to be returned'}
Sending callback to http://rest:5000/callback
Callback sent for song with hash 83abdba474adf043c6879343f3561e36d5d9b37d3dba90603b33affa2dc2a666, response status: 200
DEBUG: Waiting for messages on Redis queue...
```

## Minio Logs
```
(base) ➜  lab7-music-separation-kubernetes-prajaktakini git:(main) ✗ kubectl logs minio -f -n minio-dev
MinIO Object Storage Server
Copyright: 2015-2024 MinIO, Inc.
License: GNU AGPLv3 - https://www.gnu.org/licenses/agpl-3.0.html
Version: RELEASE.2024-11-07T00-52-20Z (go1.23.3 linux/arm64)

API: http://10.1.0.121:9000  http://127.0.0.1:9000 
WebUI: http://10.1.0.121:9090 http://127.0.0.1:9090   

Docs: https://docs.min.io
WARN: Detected default credentials 'minioadmin:minioadmin', we recommend that you change these values with 'MINIO_ROOT_USER' and 'MINIO_ROOT_PASSWORD' environment variables

```
## Video Recording
```
Access it using link: https://tinyurl.com/dcsclab7
```