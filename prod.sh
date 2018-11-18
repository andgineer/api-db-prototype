#!/usr/bin/env bash
docker build -t=back-prototype .
docker run -it -p 5000:5000 back-prototype
