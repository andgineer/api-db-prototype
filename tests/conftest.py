import os; os.environ['FLASK_ENV'] = 'testing'  # set testing env before importing app
from settings import ConfigTestWrong, ConfigTestPureFlask  #, ConfigTestTransmute, ConfigTestConnexion
import db.conn
import db.models
import settings
import pytest
from controllers.models import SUCCESS_CODES
import controllers.models
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
import json


DEFAULT_USERS = 1  # pre-created admin@


def headers(token):
    return {
        'Content-Type': "application/json",
        'Authorization': f"Bearer {token}"
    }


def get_result_data(resp, expected_statuses=SUCCESS_CODES) -> dict:
    """
    Parse reply body as json and checks ['success']
    """
    if resp.data:
        result = json.loads(resp.data)
    else:
        result = None
    assert resp.status_code in expected_statuses, \
        f'API request result with unxpected status {resp.status_code}: {resp.data}'
    return result


@pytest.fixture(scope='function', params=[ConfigTestPureFlask])  # , ConfigTestConnexion, ConfigTestTransmute])
def config(request):
    settings.config = request.param()


@pytest.fixture(scope='function', params=[ConfigTestWrong])
def config_wrong(request):
    settings.config = request.param()


@pytest.fixture(scope='function')
def api_client(config):
    db.conn.make_session()
    client = settings.config.app.test_client()
    ctx = settings.config.app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture(scope='function')
def session(config):
    db.conn.make_session()

    yield db.conn.session


@pytest.fixture(scope='function')
def wrong_session(config_wrong):
    with pytest.raises(ValueError) as e:
        db.conn.make_session()


def now_plus_two():
    return settings.config.date_to_rfc3339(settings.config.now() + timedelta(days=2))


@pytest.fixture(scope='session')
def users():
    """
    List of user's dicts
    """
    return [
        {
            'name': 'Cathy', 'email': 'cathy@',
            'group': 'guest', 'password': '12345'
        },
        {
            'name': 'Marry', 'email': 'marry@',
            'group': 'guest', 'password': '12345'
        },
        {
            'name': 'John', 'email': 'john@',
            'group': 'guest', 'password': '12345'
        },
    ]


@pytest.fixture(scope='session', params=[
    lambda: # some values would be available only at test run not at fixture creation time
    {'email': 'cathy@', 'group': 'guest'}
])
def nopassword_user(request):
    """
    User without password
    """
    return request.param()


@pytest.fixture(scope='session', params=[
    lambda:
    {
        'email': settings.config.default_admin_email,
        'group': controllers.models.ADMIN_ACCESS_GROUP,
        'password': settings.config.default_admin_password}
])
def admin_user(request):
    """
    Default admin user
    """
    return request.param()


@pytest.fixture(scope='session', params=[
    lambda:
    {
        'email': 'full@',
        'group': controllers.models.FULL_ACCESS_GROUP,
        'password': 'full',
    }
])
def full_user(request):
    """
    Full-type user
    """
    return request.param()


@pytest.fixture(scope='session', params=[
    lambda:
    {
        'email': 'demo@',
        'group': controllers.models.GUEST_ACCESS_GROUP,
        'password': 'demo',
    }
])
def demo_user(request):
    """
    demo-type user
    """
    return request.param()


@pytest.fixture(scope='session', params=[
    lambda:
    {
        'email': 'cathy@', 'group': 'guest',
        'password': '12345'
    },
    lambda:
    {
        'email': 'cathy@', 'group': 'guest',
        'name': 'Cathy', 'password': '12345'
    },
])
def user(request):
    """
    A user's dict
    """
    return request.param()


@pytest.fixture(scope='session', params=[
    lambda:
    {'email': 'cathy@', 'group': 'guest', 'status': 'full'},
    lambda:
    {'email': 'cathy@', 'group': 'guest', 'unknown': 'full'},
    lambda:
    {
        'email': 'cathy@', 'group': 'guest',
        'name': 'Cathy', 'id': '1'
    },
])
def wrong_user(request):
    """
    Wrong user's dict (without password, with fields not in spec like 'id')
    """
    return request.param()


@pytest.fixture(scope='function')
def admin_token(api_client):
    """
    JWT for admin
    """
    with api_client as client:
        resp = client.post(
            '/auth',
            data=json.dumps({'email': 'admin@', 'password': 'admin'}),
            content_type='application/json'
        )
        data = get_result_data(resp)
        return data['token']



@pytest.fixture(scope='function')
@patch('settings.config.now')
def admin_token_for_life(mock_now, api_client):
    """
    JWT for admin valid for long time
    """
    mock_now.return_value = datetime.now(timezone.utc) + timedelta(days=7)
    with api_client as client:
        resp = client.post(
            '/auth',
            data=json.dumps({'email': 'admin@', 'password': 'admin'}),
            content_type='application/json'
        )
        data = get_result_data(resp)
        return data['token']


@pytest.fixture(scope='function')
def full_token(api_client, full_user, admin_token):
    """
    JWT for full user (non-admin)
    """
    with api_client as client:
        resp = client.post(
            '/users',
            data=json.dumps(full_user),
            headers=headers(admin_token))
        get_result_data(resp)
        resp = client.post(
            '/auth',
            data=json.dumps({'email': full_user['email'], 'password': full_user['password']}),
            content_type='application/json')
        data = get_result_data(resp)
        return data['token']


@pytest.fixture(scope='function')
def demo_token(api_client, demo_user, admin_token):
    """
    JWT for demo user (non-admin)
    """
    with api_client as client:
        resp = client.post(
            '/users', data=json.dumps(demo_user), headers=headers(admin_token)
        )
        get_result_data(resp)
        resp = client.post(
            '/auth',
            data=json.dumps({'email': demo_user['email'], 'password': demo_user['password']}),
            content_type='application/json'
        )
        data = get_result_data(resp)
        return data['token']

