import pytest
from config import ConfigTestFlask, ConfigTestSwagger, ConfigTestTransmute, ConfigTestWrong
import db.conn
import db.models
from flask import Flask


@pytest.fixture(scope='function', params=[ConfigTestFlask, ConfigTestTransmute, ConfigTestSwagger])
def api_client(request):
    config = request.param()
    db.conn.make_session(config)
    db.conn.refresh_metadata()
    app = config.app
    flask_app = app if isinstance(app, Flask) else app.app  # connexions hides flask app inside connexions app
    #app.config['TESTING'] = True
    client = flask_app.test_client()
    ctx = flask_app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()
    #os.unlink(app.config['DATABASE'])


@pytest.fixture(scope='function', params=[ConfigTestFlask])
def session(request):
    db.conn.make_session(request.param())
    db.conn.refresh_metadata()

    yield db.conn.session


@pytest.fixture(scope='function', params=[ConfigTestWrong])
def wrong_session(request):
    with pytest.raises(ValueError) as e:
        db.conn.make_session(request.param())


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
def user():
    """
    A user's dict
    """
    return {'name': 'Cathy', 'email': 'cathy@'}


@pytest.fixture(scope='session')
def projects():
    """
    List of projects's names
    """
    return [{'name': 'IT'}, {'name': 'Financial'}, {'name': 'Failed'}]
