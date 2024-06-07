#!/bin/bash

# Update and install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# Pull the latest image from Docker Hub
docker-compose pull

# Run the Docker containers
docker-compose up -d
