from hypothesis import given, settings
from hypothesis import strategies as st
from string import ascii_letters, digits
from conftest import get_result_data, headers, DEFAULT_USERS
import json
import urllib.parse


@given(wrong_token=st.text(alphabet=ascii_letters+digits))
@settings(max_examples=10)
def test_users_list_wrong_token(api_client, wrong_token):
    """
    Users list with wrong token
    """
    with api_client as client:
        resp = client.get('/users', headers=headers(wrong_token))
        get_result_data(resp, expected_statuses=[401])


def test_users_list_nonadmin_token(api_client, full_token):
    """
    Users list with non-admin token
    """
    with api_client as client:
        resp = client.get('/users', headers=headers(full_token))
        get_result_data(resp, expected_statuses=[403])


def test_users_list_empty(api_client, admin_token):
    """
    Empty db returns empty user list
    """
    with api_client as client:
        resp = client.get('/users', headers=headers(admin_token))
        data = get_result_data(resp)
        assert len(data) == DEFAULT_USERS


def test_users_list_wrong_page(api_client, admin_token):
    """
    Reguest user list with page=0
    """
    with api_client as client:
        resp = client.get(f'/users?{urllib.parse.urlencode(dict(page=0))}', headers=headers(admin_token))
        get_result_data(resp, expected_statuses=[501])


def test_users_list_wrong_per_page(api_client, admin_token):
    """
    Reguest user list with per_page=0
    """
    with api_client as client:
        resp = client.get(f'/users?{urllib.parse.urlencode(dict(per_page=0))}', headers=headers(admin_token))
        get_result_data(resp, expected_statuses=[501])


def test_users_list_columns(api_client, users, admin_token):
    """
    Creates users and check API request user list
    """
    for user in users:
        with api_client as client:
            client.post('/users', data=json.dumps(user), headers=headers(admin_token))

    with api_client as client:
        resp = client.get('/users', headers=headers(admin_token))
        data = get_result_data(resp)
        assert len(data) == len(users) + DEFAULT_USERS
        user_dict = {user['email']: user for user in data}
        for user in users:
            assert user['email'] in user_dict
            list_user = user_dict[user['email']]
            assert list_user['name'] == user['name']
            assert list_user['group'] == user['group']
            assert 'password' not in list_user
            assert 'password_hash' not in list_user



