#!/usr/bin/env bash
#
# Run load tests (URL in load.yaml)
#

docker run \
    -v $(pwd):/var/loadtest \
    --net host \
    -it direvius/yandex-tank

