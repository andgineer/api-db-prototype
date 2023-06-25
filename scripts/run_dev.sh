#!/usr/bin/env bash
echo
echo "Run developer version of api server"
echo

# uncomment to create the log folder once
# we use prod settings so is is in the folder with admin access
# and we comment it because do not want to be asked for root password anytime we run dev server
# sudo mkdir -p /var/log/adp/
# sudo chown $(id -u) /var/log/adp

cd src && FLASK_ENV=development python app.py
