#!/bin/bash

sudo docker build -t server ./

# Check if the container is running
if [ "$(sudo docker ps -q -f name=server)" ]; then
    # If it is running, stop it
    sudo docker kill server
fi

sleep 1

sudo docker run -p 2016:2016 -p 2016:2016/udp --rm --name server server
