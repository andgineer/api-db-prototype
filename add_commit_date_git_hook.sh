#!/usr/bin/env bash
#
# Creates file with git commit datetime so application can show current version 'build' time
# Use hook_install.sh to install
#
FILE=src/build_timestamp
date "+%F %T" > $FILE
echo "$1" >> $FILE
git add src/build_timestamp
