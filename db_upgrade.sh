#!/usr/bin/env bash
echo
echo "Runs migrations from alembic/versions that are not applyed to the db decribed in src/db.py"
echo
alembic upgrade head
