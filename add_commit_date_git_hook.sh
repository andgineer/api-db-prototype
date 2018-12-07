#!/usr/bin/env bash
#
# Creates file with git commit datetime so application can show current version 'build' time
# Use hook_install.sh to install
#
date "+%F %T" > src/build_timestamp
git add src/build_timestamp
