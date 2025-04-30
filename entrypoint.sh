#!/bin/sh

gunicorn -w 1 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:5000 \
  --log-level debug\
  app:app

# Keep the script running to keep the container alive
tail -f /dev/null
