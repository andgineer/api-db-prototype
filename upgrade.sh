#!/usr/bin/env bash
#
# Upgrades python packages in virtual environment according requirements.txt
#

VENV_FOLDER="venv"

RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

if [[ `which python` != $PWD"/"$VENV_FOLDER"/bin/python" ]] ; then
    echo -e $RED"Please start virtual environment with"$NC
    echo ". ./activate.sh"
    exit 1
fi

pip install -r requirements.txt --upgrade
