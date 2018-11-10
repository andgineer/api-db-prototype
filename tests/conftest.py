import pytest
import app
from config import ConfigTest
import db.conn
import db.models
import controllers.db
import sqlalchemy.orm


flask_app = app.app.app  # connexions hides flask app inside connexions app


def pytest_make_parametrize_id(config, val):
    if isinstance(val, sqlalchemy.orm.Session):
        return val.get_bind().url
    return repr(val)


@pytest.fixture(scope='function')
def api_client():
    controllers.db.session = db.conn.make_session(ConfigTest())
    controllers.db.models = db.models
    db.conn.refresh_metadata(controllers.db.session)
    #app.config['TESTING'] = True
    client = flask_app.test_client()
    ctx = flask_app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()
    #os.unlink(app.config['DATABASE'])


@pytest.fixture(scope='function')
def session():
    controllers.db.session = db.conn.make_session(ConfigTest())
    controllers.db.models = db.models
    db.conn.refresh_metadata(controllers.db.session)

    yield controllers.db.session


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
