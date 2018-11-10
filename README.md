[![Build Status](https://travis-ci.org/masterandrey/api-db-prototype.png)](https://travis-ci.org/masterandrey/api-db-prototype)
.. image:: https://coveralls.io/repos/github/masterandrey/api-db-prototype/badge.svg?branch=master
   :target: https://coveralls.io/github/masterandrey/api-db-prototype?branch=master 
   :alt: Coverage
# Prototype for API

* swagger doc auto generation [transmute](https://github.com/toumorokoshi/flask-transmute)
* DB [SQLAlchemy](http://wiki.python.su/%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D0%B8/SQLAlchemy)
* [alembic](https://pypi.org/project/alembic/) for DB metadata versioning
* flask
* [flask-login](https://flask-login.readthedocs.io/en/latest/)
* [jwt](https://realpython.com/token-based-authentication-with-flask/)

To create objects in empty DB use `create_db.sh`.
The DB conect string is in `src/db.py`.

API description generated as `localhost:5000/swagger` (see `api_doc.sh`)



