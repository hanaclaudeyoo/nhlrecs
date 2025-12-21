#!/bin/bash

PACKAGE=claudehana
MODULE=nhlrecs
TAG="latest"

docker stop ${MODULE}
docker rm ${MODULE}

# docker run --rm -p 6003:7860 \
docker run --restart unless-stopped -d -p 6003:7860 \
    -e VITE_APP_NODE_ENV="prod" \
    -v $PWD/datasets:/home/app/datasets \
    --name ${MODULE} \
    ${PACKAGE}/${MODULE}:${TAG} 
