#!/usr/bin/env bash
python3.7 -m pytest -s -v --ignore src/alembic --ignore src/app.py --ignore swagger-codegen --doctest-modules src -v --cov src --cov-report term-missing -W ignore::DeprecationWarning
