#!/bin/bash

echo 'Cleaning up any Redis containers with tag "pyscrape-redis"...'
docker rm -f pyscrape-redis

echo 'Spinning up a Redis container with tag "pyscrape-redis"...'
export DOCKER_REDIS_CONTAINER=`docker run -p 127.0.0.1:6379:6379 --name pyscrape-redis -d redis`

echo 'Redis listening on: '
docker port $DOCKER_REDIS_CONTAINER
