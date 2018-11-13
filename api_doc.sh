#!/usr/bin/env bash
echo
echo "Show auto-generated OpenAPI UI"
echo "only for *-transmute version of app"
echo
cd src
python3.7 app_transmute.py &
sensible-browser "http://localhost:5000/swagger"
cd ..