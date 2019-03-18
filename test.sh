#!/usr/bin/env bash
#
# Run all tests
# To filter by test name use test.sh -k <test name>
# To filter by test marks use test.sh -m "mark1 and mark2"
#
python3.7 -m pytest -s -v -W ignore::DeprecationWarning tests $@

