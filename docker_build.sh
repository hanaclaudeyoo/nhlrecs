#!/bin/bash

# ARCH=$(dpkg --print-architecture)

PACKAGE=claudehana
MODULE=nhlrecs
DOCKERFILE="Dockerfile"
TAG="latest"
# PLATFORM="linux/${ARCH}"
PLATFORM="linux/amd64"

###rm -f .env
###DOCKER_BUILDKIT=0 docker build --platform ${PLATFORM} -f ${DOCKERFILE} --tag ${PACKAGE}/${MODULE}:${TAG} .
docker build --platform ${PLATFORM} -f ${DOCKERFILE} --tag ${PACKAGE}/${MODULE}:${TAG} .
