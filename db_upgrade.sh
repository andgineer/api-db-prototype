#!/usr/bin/env bash
echo
echo "Runs migrations from alembic/versions that are not applyed to the db decribed in src/db.py"
echo
cd src
alembic upgrade head
cd ..
