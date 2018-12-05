"""
API clients.
Corresponds to routing in server/flask_server/api_app.py
"""
from controllers.models import HttpCode
import json
from json.decoder import JSONDecodeError
import urllib.parse
from unittest.mock import patch
import contextlib


client = None  # Injection for client to send HTTP requests. It can be flask test client or requests
api_url = None # Injection for api url. It's relational for flask test client, and this is full path for requests. 


def headers(token=None):
    if token is not None:
        return {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {token}"
        }
    else:
        return {
            'Content-Type': "application/json"
        }


def parse_api_reply(resp, expected_statuses=HttpCode.successes) -> dict:
    """
    Parse reply body as json and checks ['success']
    """
    if hasattr(resp, 'data'):
        data = resp.data  # flask test client
    else:
        data = resp.text  # requests
    if data:
        try:
            result = json.loads(data)
        except JSONDecodeError as e:
            assert False, f'\n\nCannot parse as JSON reply:\n\n{data}\n\n{e}\n'
    else:
        result = None
    assert resp.status_code in expected_statuses, \
        f'API request result with unxpected status {resp.status_code}: {data}'
    return result


def get_token(email, password, expected_statuses=HttpCode.successes):
    resp = client.post(
        f'{api_url}/auth',
        data=json.dumps({'email': email, 'password': password}),
        headers=headers()
    )
    data = parse_api_reply(resp, expected_statuses=expected_statuses)
    if expected_statuses == HttpCode.successes:
        assert 'user' in data
        return data['token']
    else:
        return None


def create_user(token, user, expected_statuses=HttpCode.successes, patch_email=True):
    with patch('cloud_services.send_email', return_value=None) if patch_email else contextlib.nullcontext():
        resp = client.post(f'{api_url}/users', data=json.dumps(user), headers=headers(token))
    return parse_api_reply(resp, expected_statuses=expected_statuses)


def get_user(token, id, expected_statuses=HttpCode.successes):
    resp = client.get(f'{api_url}/users/{id}', headers=headers(token))
    return parse_api_reply(resp, expected_statuses=expected_statuses)


def update_user(token, user, id, expected_statuses=HttpCode.successes, patch_email=True):
    with patch('cloud_services.send_email', return_value=None) if patch_email else contextlib.nullcontext():
        resp = client.put(f'{api_url}/users/{id}', data=json.dumps(user), headers=headers(token))
    return parse_api_reply(resp, expected_statuses=expected_statuses)


def users_list(token, expected_statuses=HttpCode.successes, **kwargs):
    url = f'{api_url}/users'
    if kwargs:
        url += f'?{urllib.parse.urlencode(kwargs)}'
    resp = client.get(url, headers=headers(token))
    return parse_api_reply(resp, expected_statuses=expected_statuses)


def delete_user(token, id, expected_statuses=HttpCode.successes):
    resp = client.delete(f'{api_url}/users/{urllib.parse.quote(str(id))}', headers=headers(token))
    parse_api_reply(resp, expected_statuses=expected_statuses)
