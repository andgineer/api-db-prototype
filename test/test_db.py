import models
from db import db
import os
import os.path
import tempfile
from flask import json
import pytest
from src.create_app import app
from db import db


@pytest.fixture
def empty_db():
    db_file_object, db_file_name = tempfile.mkstemp()
    db.file_name = db_file_name
    db.open()

    yield None

    os.close(db_file_object)


def test_db(empty_db):
    it_project = models.Project(name='IT')
    financial_project = models.Project(name='Financial')
    db.session.add(it_project)
    db.session.add(financial_project)

    cathy = models.User(name='Cathy', email='cathy@')
    marry = models.User(name='Marry', email='marry@')
    john = models.User(name='John', email='john@')
    db.session.add(cathy)
    db.session.add(marry)
    db.session.add(john)

    cathy.projects.append(financial_project)
    marry.projects.append(financial_project)
    john.projects.append(it_project)
    john.projects.append(financial_project)

    assert db.session.query(models.User).count() == 3
