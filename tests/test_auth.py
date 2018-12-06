from flask import json
from conftest import DEFAULT_USERS
from hypothesis import settings
from unittest.mock import patch
import datetime
from datetime import timezone
import settings
import api


def test_admin_auth_fail():
    """
    Get jwt for admin default user with wrong password.
    """
    api.get_token('admin@', 'admi', expected_statuses=[403])


def test_admin_auth_success(admin_token):
    """
    Get jwt for admin default user and use it.
    """
    assert len(admin_token) > 20
    assert len(api.users_list(admin_token)) == DEFAULT_USERS


@patch('settings.config.now')
def test_expired_token(mock_now, admin_token):
    """
    Mock time so jwt should be expired.
    """
    mock_now.return_value = datetime.datetime.now(timezone.utc) + settings.config.token_expiration_delta
    api.users_list(admin_token, expected_statuses=[501])
