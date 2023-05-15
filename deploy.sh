#!/bin/bash

CONTAINER_NAME=kaaskroketbot
IMAGE_NAME=mat-ijs/kaaskroketbot

docker stop $CONTAINER_NAME
docker container rm $CONTAINER_NAME
docker image rm $IMAGE_NAME

docker build -t $IMAGE_NAME /home/pi/bots/kaaskroketbot
docker run -d --name $CONTAINER_NAME -v /var/run/docker.sock:/var/run/docker.sock --env TZ="Europe/Amsterdam" --restart unless-stopped $IMAGE_NAME