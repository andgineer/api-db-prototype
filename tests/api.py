"""
API clients.
Corresponds to routing in server/flask_server/api_app.py
"""
import contextlib
import json
import urllib.parse
from json.decoder import JSONDecodeError
from unittest.mock import patch

from controllers.models import HttpCode

client = (
    None  # Injection for client to send HTTP requests. It can be flask test client or requests
)
api_url = None  # Injection for api url. It's relational for flask test client, and this is full path for requests.
verify_ssl = None  # Set it only for requests

last_response = None  # Last response to api call


def add_verify(kwargs):
    if verify_ssl is not None:
        kwargs["verify"] = verify_ssl
    return kwargs


def post(*args, env=None, **kwargs):
    # if 'verify' in kwargs:
    #     del kwargs['verify']
    if env is None:
        env = {}
    else:
        env = {"environ_base": env}
    return client.post(*args, **env, **add_verify(kwargs))


def get(*args, env=None, **kwargs):
    # if 'verify' in kwargs:
    #     del kwargs['verify']
    if env is None:
        env = {}
    else:
        env = {"environ_base": env}
    return client.get(*args, **env, **add_verify(kwargs))


def put(*args, **kwargs):
    # if 'verify' in kwargs:
    #     del kwargs['verify']
    return client.put(*args, **add_verify(kwargs))


def delete(*args, **kwargs):
    # if 'verify' in kwargs:
    #     del kwargs['verify']
    return client.delete(*args, **add_verify(kwargs))


def options(*args, **kwargs):
    # if 'verify' in kwargs:
    #     del kwargs['verify']
    return client.options(*args, **add_verify(kwargs))


def headers(token=None):
    if token is not None:
        return {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    else:
        return {"Content-Type": "application/json"}


def parse_api_reply(resp, expected_statuses=HttpCode.successes) -> dict:
    """
    Parse reply body as json and checks ['success']
    """
    global last_response
    last_response = resp

    if hasattr(resp, "data"):
        data = resp.data  # flask test client
    else:
        data = resp.text  # requests
    if data:
        try:
            result = json.loads(data)
        except JSONDecodeError as e:
            assert False, f"\n\nCannot parse as JSON reply:\n\n{data}\n\n{e}\n"
    else:
        result = None
    assert (
        resp.status_code in expected_statuses
    ), f"API request result with unxpected status {resp.status_code}: {data}"
    return result


def get_token(email, password, expected_statuses=HttpCode.successes):
    resp = post(
        f"{api_url}/auth",
        data=json.dumps({"email": email, "password": password}),
        headers=headers(),
    )
    data = parse_api_reply(resp, expected_statuses=expected_statuses)
    return data["token"] if expected_statuses == HttpCode.successes else None


def create_user(token, user, expected_statuses=HttpCode.successes, patch_email=True):
    with patch(
        "cloud_services.send_email", return_value=None
    ) if patch_email else contextlib.nullcontext():
        resp = post(
            f"{api_url}/users", data=json.dumps({"new_user": user}), headers=headers(token)
        )
    return parse_api_reply(resp, expected_statuses=expected_statuses)


def get_user(token, id, expected_statuses=HttpCode.successes):
    resp = get(f"{api_url}/users/{id}", headers=headers(token))
    return parse_api_reply(resp, expected_statuses=expected_statuses)


def update_user(token, user, id, expected_statuses=HttpCode.successes, patch_email=True):
    with patch(
        "cloud_services.send_email", return_value=None
    ) if patch_email else contextlib.nullcontext():
        resp = put(f"{api_url}/users/{id}", data=json.dumps(user), headers=headers(token))
    return parse_api_reply(resp, expected_statuses=expected_statuses)


def users_list(token, expected_statuses=HttpCode.successes, **kwargs):
    url = f"{api_url}/users"
    if kwargs:
        url += f"?{urllib.parse.urlencode(kwargs)}"
    resp = get(url, headers=headers(token))
    data = parse_api_reply(resp, expected_statuses=expected_statuses)
    if expected_statuses == HttpCode.successes:
        return data["data"]
    else:
        return None


def delete_user(token, id, expected_statuses=HttpCode.successes):
    resp = delete(f"{api_url}/users/{urllib.parse.quote(str(id))}", headers=headers(token))
    parse_api_reply(resp, expected_statuses=expected_statuses)


def get_options(path):
    resp = options(f"{api_url}/{path}")
    assert resp.status_code in [200, 204]
    return resp
