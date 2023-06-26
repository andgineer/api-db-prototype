#!/usr/bin/env bash
#
# Run load tests (URL in load.yaml)
#

docker run \
    -v $(pwd)/stress:/var/loadtest \
    --net host \
    -it direvius/yandex-tank
