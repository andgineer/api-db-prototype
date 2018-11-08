import pytest
from src.api import app
from config import ConfigTest
from db import db


@pytest.fixture(scope='session')
def api_client():
    #app.config['TESTING'] = True
    client = app.test_client()
    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()
    #os.unlink(app.config['DATABASE'])


@pytest.fixture(scope='function')
def empty_db():
    db.connect(ConfigTest())
    db.create_meta()
    yield None


@pytest.fixture(scope='session')
def user():
    """
    One user dict.
    """
    return {'name': 'John', 'email': 'john@'}


@pytest.fixture(scope='session')
def users():
    """
    List of user's dicts
    """
    return [
        {'name': 'Cathy', 'email': 'cathy@'},
        {'name': 'Marry', 'email': 'marry@'},
        {'name': 'John', 'email': 'john@'},
    ]


@pytest.fixture(scope='session')
def projects():
    """
    List of projects's names
    """
    return [{'name': 'IT'}, {'name': 'Financial'}, {'name': 'Failed'}]
