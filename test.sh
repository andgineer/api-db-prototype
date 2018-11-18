#!/usr/bin/env bash
python3.7 -m pytest -s -v -W ignore::DeprecationWarning $@

