#!/bin/bash

# Set env variables
IMAGE_NAME=dev_grocery_ocr_api
APP_NAME=dev_grocery_ocr_api

# stop and remove image in case this script was run before
if docker ps -a --format "{{.Names}}" | grep -q "^${APP_NAME}$"; then
    docker stop ${APP_NAME}
    docker rm ${APP_NAME}
fi

# Build your Docker container
docker build -t ${IMAGE_NAME} .

# Run your built container in detached mode
docker run -d --name ${APP_NAME} -p 8000:8000 ${IMAGE_NAME}

# wait for the /health endpoint to return a 200 and then move on
finished=false
while ! $finished; do
    health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health")
    if [ $health_status == "200" ]; then
        finished=true
        echo "API is ready"
    else
        echo "API not responding yet"
        sleep 5
    fi
done