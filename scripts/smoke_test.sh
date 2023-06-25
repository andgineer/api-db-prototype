#!/usr/bin/env bash
#
# Quick curl test
# Requests JWT and after that requests user list with it
#
case $1 in
     local)
          URL=http://localhost:5000
          ADMIN_EMAIL="admin@"
          ;;
     dev)
          URL=https://example.com
          ADMIN_EMAIL="???@example.com"
          ;;
     *)
          echo
          echo "Quick smoke test"
          echo "Usage:"
          echo "quick_test.sh local - test local server"
          echo "quick_test.sh dev - test external server"
          echo
          echo
          echo "You should specify local or dev"
          echo
          exit
          ;;
esac

RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color
NL=$'\n'

echo
echo -e $CYAN"..requesting security token from ${URL} for ${ADMIN_EMAIL}..."$NC
echo
TOKEN=$(curl -s -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -X POST \
    -d '{"email": "'${ADMIN_EMAIL}'", "password": "admin"}' \
    ${URL}/auth | \
    python3 -c $'
import sys, json
from json.decoder import JSONDecodeError
try:
    reply = sys.stdin.read()
    print(json.loads(reply)[\'token\'])
except JSONDecodeError:
    print(reply)
    exit(1)
')

if [ $? -eq 0 ]
then
  echo -e $GREEN"success!"$NC

echo
echo -e $CYAN"..requesting user list..."$NC
echo
curl -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" ${URL}/users?per_page=1

if [ $? -eq 0 ]
then
  echo
  echo -e $GREEN"success!"$NC
  echo
else
  echo -e $RED"failed"$NC
fi

else
  echo -e $RED"failed: "$TOKEN$NC
fi

#curl -s -H 'Accept: application/json' \
#    -H "Content-Type: application/json" \
#    -X POST \
#    -H "Authorization: Bearer ${TOKEN}" \
#    -d '{"newUser": {"email": "Andrei_Sorokin2@epam.com", "password": "admin", "type": "admin", "expiration": "2058-01-01"}}' \
#    ${URL}/api/users
