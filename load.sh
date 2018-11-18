#!/usr/bin/env bash
docker run \
    -v $(pwd):/var/loadtest \
    --net host \
    -it direvius/yandex-tank

