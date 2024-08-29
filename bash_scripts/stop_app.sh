#!/bin/bash

# Set env variables
IMAGE_NAME=dev_grocery_ocr_api
APP_NAME=dev_grocery_ocr_api

# Kill the running container
docker stop ${APP_NAME}

# Delete the built Docker container
docker rm ${APP_NAME}
docker image rm ${APP_NAME}