import os
import os.path
import tempfile
from flask import json
import pytest
from src.create_app import app
from db import db


@pytest.fixture
def api_client():
    db_file_object, db_file_name = tempfile.mkstemp()
    db.file_name = 'test.sqlite'  # db_file_name
    db.open()

    #app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_file_object)
    #os.unlink(app.config['DATABASE'])


def test_api(api_client):
    with api_client as c:
        resp = c.get('/users')
        data = json.loads(resp.data)
        assert data['success']
        assert data['result'] == []
