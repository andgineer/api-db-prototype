#!/usr/bin/env bash
cd src
python3.7 app.py &
sensible-browser "http://localhost:5000/swagger"
cd ..