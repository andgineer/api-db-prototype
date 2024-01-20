#!/usr/bin/env bash
#
# Builds docker image and run it
#
docker build -t=backend .
docker rm backend --force 2> /dev/null
# on prod server use -d instead of -it
docker run --rm -it --name backend -p 5000:5000 --volume $PWD/logs:/var/log/adp backend
