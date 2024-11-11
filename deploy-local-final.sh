#!/bin/sh

# setting up minio
kubectl apply -f minio/minio-dev.yaml # Apply pod YAML
kubectl apply -f minio/minio-service.yaml # Apply service YAML
sleep 5

# setting up logs
kubectl apply -f logs/logs-deployment.yaml
sleep 5

# setting up redis (want before rest)
kubectl apply -f redis/redis-deployment.yaml # Apply Deployment YAML
kubectl apply -f redis/redis-service.yaml # Apply service YAML
sleep 5

# deploying rest server (connects to minio & redis)
kubectl apply -f rest/rest-deployment.yaml # Apply Deployment YAML
kubectl apply -f rest/rest-service.yaml # Apply service YAML
sleep 5

# deploy worker
kubectl apply -f worker/worker-deployment.yaml # Apply Deployment YAML
kubectl apply -f worker/worker-service.yaml # Apply service YAML # worker may not need it as we don't call any endpoint on worker
sleep 5


# forwarding ports (redis/rest/minio)
kubectl port-forward --address 0.0.0.0 service/redis 6380:6379 & # Redis port forwarding # for checking connections
kubectl port-forward --address 0.0.0.0 service/rest 5001:5000 & # REST port forwarding for invoking endpoints
kubectl port-forward -n minio-dev --address 0.0.0.0 service/minio 9090:9090 & # Minio port forwarding for accessing Web UI