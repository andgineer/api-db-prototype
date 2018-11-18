#!/usr/bin/env bash
python3.7 -m pytest -s -v -W ignore::DeprecationWarning --doctest-modules server -v --cov server --cov-report term-missing
