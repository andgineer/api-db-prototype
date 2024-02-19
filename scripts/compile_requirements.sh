#!/usr/bin/env bash
#
# Pin current dependencies versions.
#

START_TIME=$(date +%s)

uv pip compile requirements.dev.in
REQS_DEV_TIME=$(date +%s)

uv pip compile requirements.in
REQS_TIME=$(date +%s)

uv pip compile requirements.prod.in
END_TIME=$(date +%s)

echo "Req‘s dev compilation time: $((REQS_DEV_TIME - $START_TIME)) seconds"
echo "Req‘s compilation time: $((REQS_TIME - $REQS_DEV_TIME)) seconds"
echo "Req‘s prod compilation time: $((END_TIME - $REQS_TIME)) seconds"
echo "Total execution time: $((END_TIME - $START_TIME)) seconds"
