#!/usr/bin/env bash
#
# Creates file with git commit datetime so application can show current version 'build' time
# Use git_hook_install.sh to install
#
FILE=src/build_timestamp
date "+%F %T" > "$FILE"
#cat "$1" >> "$FILE" this is for commit-msg but I do not see how to add file to commit at this stage
git add "$FILE"
