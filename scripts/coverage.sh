#!/usr/bin/env bash
python3.7 -m pytest -s -v --doctest-modules \
    --cov src --cov-report term-missing \
    --ignore src/alembic \
    --ignore swagger-codegen \
    --ignore src/flask_server/api_app.py \
    -W ignore::DeprecationWarning
