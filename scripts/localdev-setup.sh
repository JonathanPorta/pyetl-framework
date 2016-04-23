#!/bin/bash

pyvenv-3.4 env

echo 'Please activate the environment: `source env/bin/activate`'

docker rm -f pyscrape-redis
export DOCKER_REDIS_CONTAINER=`docker run -p 127.0.0.1:6379:6379 --name pyscrape-redis -d redis`

echo 'Redis listening on: '
docker port $DOCKER_REDIS_CONTAINER
