#!/usr/bin/env bash
#
# Run all tests
# To filter by test name use test.sh -k <test name>
# To filter by test marks use test.sh -m "mark1 and mark2"
#
# (!) do not forget to activate virtual env and install dependencies:
#   . ./activate.sh
#
python -m pytest \
  --cov src \
  --ignore src/alembic \
  --ignore swagger-codegen \
  -W ignore::DeprecationWarning \
   tests/ \
  "$@"
