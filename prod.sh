#!/usr/bin/env bash
#
# Builds docker image and run it with uWSGI
#
docker build -t=backend .
docker stop backend
docker rm backend
docker run -d --name backend -p 5000:5000 --volume $PWD/logs:/var/log/adp backend

