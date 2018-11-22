from flask import json
from conftest import get_result_data, headers, DEFAULT_USERS
from hypothesis import settings
from unittest.mock import patch
import datetime
from datetime import timezone
import settings


def test_admin_auth_fail(api_client):
    """
    Get jwt for admin default user with wrong password.
    """
    with api_client as client:
        resp = client.post(
            '/auth',
            data=json.dumps({'email': 'admin@', 'password': 'admi'}),
            content_type='application/json'
        )
        get_result_data(resp, expected_statuses=[403])


def test_admin_auth_success(api_client, admin_token):
    """
    Get jwt for admin default user and use it.
    """
    with api_client as client:
        assert len(admin_token) > 20
        resp = client.get('/users', headers=headers(admin_token))
        data = get_result_data(resp)
        assert len(data) == DEFAULT_USERS


@patch('settings.config.now')
def test_expired_token(mock_now, api_client, admin_token):
    """
    Mock time so jwt should be expired.
    """
    with api_client as client:
        mock_now.return_value = datetime.datetime.now(timezone.utc) + settings.config.token_expiration_delta
        resp = client.get('/users', headers=headers(admin_token))
        get_result_data(resp, expected_statuses=[501])
