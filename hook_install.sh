#!/usr/bin/env bash
#
# Installs git hook to add 'build' date to application
#
if [ ! -f .git/hooks/pre-commit ] ; then
    ln -s $PWD/add_commit_date_git_hook.sh .git/hooks/commit-msg
fi
