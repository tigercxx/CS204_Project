#!/bin/bash

sudo docker build -t client ./

# Check if the container is running
if [ "$(sudo docker ps -q -f name=client)" ]; then
    # If it is running, stop it
    sudo docker kill client
fi

sleep 1

sudo docker run --network="host" --name client --rm -d -v $(pwd)/data:/app/data client 


