import os

os.environ["SERVER_ENV"] = "testing"  # set testing env before importing app
import json
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

import api
import controllers.models
import db.conn
import db.models
import settings
from controllers.models import HttpCode
from settings import ConfigTestConnexion, ConfigTestPureFlask, ConfigTestWrong

DEFAULT_USERS = 1  # pre-created admin@
TEST_COVERAGE_REPORT_FILE = "pytest-coverage.txt"


def headers(token):
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }


def get_result_data(resp, expected_statuses=HttpCode.successes) -> dict:
    """Parse reply body as json and checks ['success']."""
    if resp.data:
        result = json.loads(resp.data)
    else:
        result = None
    assert resp.status_code in expected_statuses, (
        f"API request result with unxpected status {resp.status_code}: {resp.data}"
    )
    return result


@pytest.fixture(scope="function", params=[ConfigTestPureFlask, ConfigTestConnexion])
def config(request):
    settings.config = request.param()
    api.api_url = settings.config.api_url
    return settings.config


@pytest.fixture(scope="function", params=[ConfigTestWrong])
def config_wrong(request):
    settings.config = request.param()
    api.api_url = settings.config.api_url
    return settings.config


@pytest.fixture(scope="function", autouse=True)
def api_client(request, config):
    if "no_auto_client" in request.keywords:
        yield None  # do not auto-use for tests marked as no_auto_client
        return  # empty test tear-down
    db.conn.make_session()
    settings.config.app.testing = True
    client = settings.config.app.test_client()

    if hasattr(settings.config.app, "test_request_context"):
        ctx = settings.config.app.test_request_context()
        ctx.push()
    else:
        ctx = None

    api.client = client  # inject test client
    yield client

    if ctx is not None:
        ctx.pop()


@pytest.fixture(scope="function", params=[ConfigTestPureFlask])
def flask_config(request):
    settings.config = request.param()
    api.api_url = settings.config.api_url
    return settings.config


@pytest.fixture(scope="function")
def flask_client(flask_config):
    """Flask-only tests."""
    db.conn.make_session()
    client = settings.config.app.test_client()
    if hasattr(settings.config.app, "test_request_context"):
        ctx = settings.config.app.test_request_context()
        ctx.push()
    else:
        ctx = None

    api.client = client  # inject test client
    yield client

    if ctx is not None:
        ctx.pop()


@pytest.fixture(scope="function")
def session(config):
    db.conn.make_session()

    yield db.conn.session


@pytest.fixture(scope="function")
def wrong_session(config_wrong):
    with pytest.raises(ValueError):
        db.conn.make_session()


def now_plus_two():
    return settings.config.date_to_rfc3339(settings.config.now() + timedelta(days=2))


@pytest.fixture(scope="session")
def users():
    """List of user's dicts."""
    return [
        {"name": "Cathy", "email": "cathy@", "group": "guest", "password": "12345"},
        {"name": "Marry", "email": "marry@", "group": "guest", "password": "12345"},
        {"name": "John", "email": "john@", "group": "guest", "password": "12345"},
    ]


@pytest.fixture(
    scope="session",
    params=[
        lambda: {  # some values would be available only at test run not at fixture creation time
            "email": "cathy@",
            "group": "guest",
        }
    ],
)
def nopassword_user(request):
    """User without password."""
    return request.param()


@pytest.fixture(
    scope="session",
    params=[
        lambda: {
            "email": settings.config.default_admin_email,
            "group": controllers.models.UserGroup.ADMIN.value,
            "password": settings.config.default_admin_password,
        }
    ],
)
def admin_user(request):
    """Default admin user."""
    return request.param()


@pytest.fixture(
    scope="session",
    params=[
        lambda: {
            "email": "full@",
            "group": controllers.models.UserGroup.FULL.value,
            "password": "full",
        }
    ],
)
def full_user(request):
    """Full-type user."""
    return request.param()


@pytest.fixture(
    scope="session",
    params=[
        lambda: {
            "email": "demo@",
            "group": controllers.models.UserGroup.GUEST.value,
            "password": "demo",
        }
    ],
)
def demo_user(request):
    """Demo-type user."""
    return request.param()


@pytest.fixture(
    scope="session",
    params=[
        lambda: {"email": "cathy@", "group": "guest", "password": "12345"},
        lambda: {"email": "cathy@", "group": "guest", "name": "Cathy", "password": "12345"},
    ],
)
def user(request):
    """
    A user's dict
    """
    return request.param()


@pytest.fixture(
    scope="session",
    params=[
        lambda: {"email": "cathy@", "group": "guest", "status": "full"},
        lambda: {"email": "cathy@", "group": "guest", "unknown": "full"},
        lambda: {"email": "cathy@", "group": "guest", "name": "Cathy", "id": "1"},
    ],
)
def wrong_user(request):
    """Wrong user's dict (without password, with fields not in spec like 'id')."""
    return request.param()


@pytest.fixture(scope="function")
def admin_token(api_client):
    """JWT for admin."""
    return api.get_token(email="admin@", password="admin")


@pytest.fixture(scope="function")
@patch("settings.config.now")
def admin_token_for_life(mock_now, api_client):
    """JWT for admin valid for long time."""
    mock_now.return_value = datetime.now(timezone.utc) + timedelta(days=7)
    return api.get_token(email="admin@", password="admin")


@pytest.fixture(scope="function")
def full_token(api_client, full_user, admin_token):
    """JWT for full user (non-admin)."""
    api.create_user(admin_token, full_user)
    return api.get_token(email=full_user["email"], password=full_user["password"])


@pytest.fixture(scope="function")
def demo_token(api_client, demo_user, admin_token):
    """JWT for demo user (non-admin)."""
    api.create_user(admin_token, demo_user)
    return api.get_token(email=demo_user["email"], password=demo_user["password"])
