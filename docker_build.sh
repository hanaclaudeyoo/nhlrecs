#!/bin/bash

# ARCH=$(dpkg --print-architecture)
SYS=`uname -s`
# PLATFORM="linux/${ARCH}"
PLATFORM="linux/amd64"
if [ "$SYS" = "Darwin" ]; then  
	ARCH=`uname -m`
	PLATFORM="linux/$ARCH"
fi
echo "PLATFORM=${PLATFORM}"

PACKAGE=claudehana
MODULE=nhlrecs
DOCKERFILE="Dockerfile"
TAG="latest"

##### DOCKER_BUILDKIT=0 docker build --platform ${PLATFORM} -f ${DOCKERFILE} --tag ${PACKAGE}/${MODULE}:${TAG} .
docker build --platform ${PLATFORM} -f ${DOCKERFILE} --tag ${PACKAGE}/${MODULE}:${TAG} .
