#!/usr/bin/env bash
#
# Creates file with git commit datetime so application can show current version 'build' time
# Use git_hook_install.sh to install
#
DATE_FILE=src/build_timestamp
VER_FILE=src/build_ver
date "+%F %T" > "$DATE_FILE"
v_h=$(cat $VER_FILE | awk -F "." '{print $1 "." $2}')
v_m=$(cat $VER_FILE | awk -F "." '{print $3}')
v_m=$((v_m+1))
echo "$v_h.$v_m" > "$VER_FILE"
#cat "$1" >> "$FILE" this is for commit-msg but I do not see how to add file to commit at this stage
git add "$DATE_FILE" "$VER_FILE"
# --no-verify (avoid looping)
# git commit --amend -C HEAD --no-verify