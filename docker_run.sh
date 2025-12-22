#!/bin/bash

PACKAGE=claudehana
MODULE=nhlrecs
TAG="latest"

docker stop ${MODULE}
docker rm ${MODULE}

mkdir -p datasets

PYTHONUNBUFFERED=1

# docker run --rm -p 6003:7860 \
docker run --restart unless-stopped -d -p 6003:7860 \
    -v $PWD/datasets:/home/app/datasets \
    -e VITE_APP_NODE_ENV="prod" \
    -e PYTHONUNBUFFERED=$PYTHONUNBUFFERED \
    --name ${MODULE} \
    ${PACKAGE}/${MODULE}:${TAG} 
