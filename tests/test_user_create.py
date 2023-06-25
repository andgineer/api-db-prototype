from string import ascii_letters, digits

from hypothesis import given, settings
from hypothesis import strategies as st

import api


@given(wrong_token=st.text(alphabet=ascii_letters + digits))
@settings(max_examples=10, deadline=None)
def test_user_create_wrong_token(user, wrong_token):
    """
    Create user with wrong token
    """
    api.create_user(wrong_token, user, expected_statuses=[401])


def test_user_create_wrong_user(wrong_user, admin_token):
    """
    Tries to create user with wrong fields.
    """
    api.create_user(
        admin_token, wrong_user, expected_statuses=[501, 400]
    )  # 400 for auto exc of transmute


def test_user_create_duplicate(user, admin_token):
    """
    Tries to create duplicate users.
    """
    api.create_user(admin_token, user)
    api.create_user(admin_token, user, expected_statuses=[400])


def test_user_create_nopassword(nopassword_user, admin_token):
    """
    Tries to create user with no password.
    """
    api.create_user(
        admin_token, nopassword_user, expected_statuses=[501, 400]
    )  # 400 for auto exc of transmute


def test_user_create_by_full(user, full_token):
    """
    Tries to create user with full (non-admin) rights.
    """
    api.create_user(full_token, user, expected_statuses=[403])


def test_user_create_by_demo(user, demo_token):
    """
    Tries to create user with demo (non-admin) rights.
    """
    api.create_user(demo_token, user, expected_statuses=[403])


def test_user_create_success(user, admin_token):
    """
    Creates user.
    """
    api.create_user(admin_token, user)
