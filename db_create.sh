#!/usr/bin/env bash
echo
echo "The DB conect string is in src/db.py"
echo
cd src
python3.7 db_init.py
cd ..
