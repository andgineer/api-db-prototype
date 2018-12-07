#!/usr/bin/env bash
#
# Creates file with git commit datetime so application can show current version 'build' time
# Use hook_install.sh to install
#
date "+%F %T" > src/biuld_timestamp
git add src/biuld_timestamp
