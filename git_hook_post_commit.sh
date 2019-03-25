#!/usr/bin/env bash
DATE_FILE=src/build_timestamp
VER_FILE=src/build_ver
git add "$DATE_FILE" "$VER_FILE"
git commit --amend -C HEAD --no-verify
