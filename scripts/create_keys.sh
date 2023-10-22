#!/usr/bin/env bash
#
# Creates key and certificate in secret/
#

OUT_FOLDER=server/secret

echo
echo "Recreates key and certificate at security folder"
echo
read -p "Are you sure? [YN]" -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo
    echo "Aborting..."
    echo
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi
openssl req -x509 -newkey rsa:4096 -nodes -keyout ${OUT_FOLDER}/jwt_test_key.pem -out ${OUT_FOLDER}/jwt_test_cert.pem -days 10000
echo
echo "Result placed into ${OUT_FOLDER}"
echo
