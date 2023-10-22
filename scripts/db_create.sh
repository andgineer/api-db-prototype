#!/usr/bin/env bash
echo
echo "The DB conect string is in src/config.py"
echo
cd src
python db/init.py
cd ..
