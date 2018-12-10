from hypothesis import given, settings
from hypothesis import strategies as st
from string import ascii_letters, digits
from conftest import DEFAULT_USERS
import json
import urllib.parse
import api


@given(wrong_token=st.text(alphabet=ascii_letters+digits))
@settings(max_examples=10)
def test_users_list_wrong_token(wrong_token):
    """
    Users list with wrong token
    """
    api.users_list(wrong_token, expected_statuses=[401])


def test_users_list_nonadmin_token(full_token):
    """
    Users list with non-admin token
    """
    api.users_list(full_token, expected_statuses=[403])


def test_users_list_empty(admin_token):
    """
    Empty db returns empty user list
    """
    assert len(api.users_list(admin_token)) == DEFAULT_USERS


def test_users_list_wrong_page(admin_token):
    """
    Reguest user list with page=0
    """
    api.users_list(admin_token, page=0, expected_statuses=[501])


def test_users_list_wrong_per_page(admin_token):
    """
    Reguest user list with per_page=0
    """
    api.users_list(admin_token, per_page=0, expected_statuses=[501])


def test_users_list_columns(users, admin_token):
    """
    Creates users and check API request user list
    """
    for user in users:
        api.create_user(admin_token, user)
    data = api.users_list(admin_token)
    assert len(data) == len(users) + DEFAULT_USERS
    user_dict = {user['email']: user for user in data}
    for user in users:
        assert user['email'] in user_dict
        list_user = user_dict[user['email']]
        assert list_user['name'] == user['name']
        assert list_user['group'] == user['group']
        assert 'password' not in list_user
        assert 'password_hash' not in list_user


def test_users_list_empty_params(user, admin_token):
    """
    Test empty list params list
    """
    api.create_user(admin_token, user)
    assert len(api.users_list(admin_token, page='', per_page='', order_by='')) == 1 + DEFAULT_USERS
    api.users_list(admin_token, page='-1', expected_statuses=[501])
