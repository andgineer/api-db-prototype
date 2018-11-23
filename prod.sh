#!/usr/bin/env bash
#
# Builds docker image and run it with uWSGI
#
docker build -t=backend .
docker stop backend
docker run --name backend -it -p 5000:5000 backend
