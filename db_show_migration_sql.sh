#!/usr/bin/env bash
echo
echo "Show (without execution) migrations SQL from alembic/versions that are not applyed to the db decribed in src/db.py"
echo

alembic upgrade --sql head
