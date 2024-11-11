#!/bin/sh

# Use to build and push docker image for REST
docker build --platform linux/amd64 -t prajaktakini17/lab7-rest:v16 rest/.
docker push prajaktakini17/lab7-rest:v16

# Use to build and push docker image for Worker
docker build --platform linux/amd64 -t prajaktakini17/lab7-worker:v16 worker/.
docker push prajaktakini17/lab7-worker:v16