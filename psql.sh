#!/usr/bin/env bash
echo
echo "To save password place into file ~/.pgpass line '<DB server host>:5432:<DB file>:root:<password>'"
echo "And press <ENTER> at password prompt of psql."
echo
psql -h <DB server host> -p 5432 -U root -W <DB file>
