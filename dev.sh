#!/usr/bin/env bash
echo
echo "Run developer version of api server"
echo
# sudo mkdir -p /var/log/adp
# sudo chown $(id -u) /var/log/adp
cd src && FLASK_ENV=development python3.7 app.py
