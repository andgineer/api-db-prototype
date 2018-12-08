#!/usr/bin/env bash
#
# Installs git hook to add 'build' date to application
#
if [ ! -f .git/hooks/pre-commit ] ; then
    ln -s $PWD/git_hook_add_commit_date.sh .git/hooks/pre-commit
fi
