#! /usr/bin/env bash

ENV_NAME="<env name>"

RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

if ! (return 0 2>/dev/null) ; then
    # If return is used in the top-level scope of a non-sourced script,
    # an error message is emitted, and the exit code is set to 1
    echo
    echo -e $RED"This script should be sourced like"$NC
    echo "    . ./activate.sh"
    echo
    exit 1  # we detected we are NOT source'd so we can use exit
fi

if type conda 2>/dev/null; then
    if conda info --envs | grep ${ENV_NAME}; then
      echo -e $CYAN"activating environment ${ENV_NAME}"$NC
    else
      echo
      echo -e $RED"(!) Please install the conda environment ${ENV_NAME}"$NC
      echo
      return 1  # we are source'd so we cannot use exit
    fi
else
    echo
    echo -e $RED"(!) Please install anaconda"$NC
    echo
    return 1  # we are source'd so we cannot use exit
fi

conda activate ${ENV_NAME}
