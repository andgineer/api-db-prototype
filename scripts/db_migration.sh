#!/usr/bin/env bash
if [ -n "$1" ] && [[ "$1" =~ ^[^\-].* ]]; then
    cd src
    alembic revision --autogenerate -m "$1"
    cd ..
    echo
    echo "Migration script is in alembic/versions/...$1.py"
    echo

else

    echo
    echo "Creates DB migration script as difference between DB"
    echo "and models in src/models.py."
    echo "DB connection string is in src/db.py."
    echo
    echo "Please specify the migration name:"
    echo "db_create_migration.sh <migration name>"
    echo

fi
