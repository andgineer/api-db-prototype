[![Build Status](https://travis-ci.org/masterandrey/api-db-prototype.png)](https://travis-ci.org/masterandrey/api-db-prototype)
[![Test coverage](https://coveralls.io/repos/github/masterandrey/api-db-prototype/badge.svg?branch=master)](https://coveralls.io/github/masterandrey/api-db-prototype?branch=master)
# Prototype for API

Implements API server with different frameworks (uncomment appropriate in `app.py`):
* Transmute
* Swagger codegen (connexion)
* Pure flask

Libraries:
* swagger doc auto generation [transmute](https://github.com/toumorokoshi/flask-transmute)
* DB [SQLAlchemy](http://wiki.python.su/%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D0%B8/SQLAlchemy)
* [alembic](https://pypi.org/project/alembic/) for DB metadata versioning
* flask
* [flask-login](https://flask-login.readthedocs.io/en/latest/)
* [jwt](https://realpython.com/token-based-authentication-with-flask/)

To create objects in empty DB use `db_create.sh`.
The DB connect string is in `src/config.py`.

For `transmute_server` flavor of the app, API description generated as 
`localhost:5000/swagger` (see `api_doc.sh`).
