#!/usr/bin/env bash
echo
echo "Run developer version of api server"
echo
cd src && FLASK_ENV=development python3.7 app.py
