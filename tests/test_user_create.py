from flask import json
from conftest import get_result_data, headers
from hypothesis import given, settings
from hypothesis import strategies as st
from string import ascii_letters, digits
from unittest.mock import patch
import datetime


@given(wrong_token=st.text(alphabet=ascii_letters+digits))
@settings(max_examples=10)
def test_user_create_wrong_token(api_client, user, wrong_token):
    """
    Create user with wrong token
    """
    with api_client as client:
        resp = client.post('/users', data=json.dumps(user), headers=headers(wrong_token))
        get_result_data(resp, expected_statuses=[401])


def test_user_create_wrong_user(api_client, wrong_user, admin_token):
    """
    Tries to create user with wrong fields.
    """
    with api_client as client:
        resp = client.post('/users', data=json.dumps(wrong_user), headers=headers(admin_token))
        get_result_data(resp, expected_statuses=[501])


def test_user_create_duplicate(api_client, user, admin_token):
    """
    Tries to create duplicate users.
    """
    with api_client as client:
        resp = client.post('/users', data=json.dumps(user), headers=headers(admin_token))
        get_result_data(resp)
        resp = client.post('/users', data=json.dumps(user), headers=headers(admin_token))
        get_result_data(resp, expected_statuses=[400])


def test_user_create_nopassword(api_client, nopassword_user, admin_token):
    """
    Tries to create user with no password.
    """
    with api_client as client:
        resp = client.post('/users', data=json.dumps(nopassword_user), headers=headers(admin_token))
        get_result_data(resp, expected_statuses=[501])


def test_user_create_by_full(api_client, user, full_token):
    """
    Tries to create user with full (non-admin) rights.
    """
    with api_client as client:
        resp = client.post('/users', data=json.dumps(user), headers=headers(full_token))
        get_result_data(resp, expected_statuses=[403])


def test_user_create_by_demo(api_client, user, demo_token):
    """
    Tries to create user with demo (non-admin) rights.
    """
    with api_client as client:
        resp = client.post('/users', data=json.dumps(user), headers=headers(demo_token))
        get_result_data(resp, expected_statuses=[403])


def test_user_create_success(api_client, user, admin_token):
    """
    Creates user.
    """
    with api_client as client:
        resp = client.post('/users', data=json.dumps(user), headers=headers(admin_token))
        get_result_data(resp)
