#!/usr/bin/env bash
echo
echo "Run developer version of api server"
echo
echo "May ask for sudo password"
echo

# we use prod settings with logs in `/var` so sudo
if [ ! -d "/var/log/adp/" ]; then
    sudo mkdir -p /var/log/adp/
    sudo chown $(id -u) /var/log/adp
fi

cd src && SERVER_ENV=development python app.py
