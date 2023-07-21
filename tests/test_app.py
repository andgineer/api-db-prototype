import os
import pytest
from unittest import mock

import app
import settings
from db import conn

# Mocking the DB connection
class MockDBSession:
    def make_session(self):
        pass

# Mocking the Config Classes
class MockConfig:
    def __init__(self):
        self.app = "mock_app"
        self.port = 5000

# Patch the settings configurations
@pytest.fixture(autouse=True)
def setup_config(monkeypatch):
    monkeypatch.setattr(settings, "ConfigTest", MockConfig)
    monkeypatch.setattr(settings, "ConfigDev", MockConfig)
    monkeypatch.setattr(settings, "ConfigProd", MockConfig)
    monkeypatch.setattr(conn, "make_session", MockDBSession().make_session)

@mock.patch('app.main')
@mock.patch.dict(os.environ, {"FLASK_ENV": "development"})
def test_main_in_development_env(main_mock):
    app.main()
    main_mock.assert_called_once()

@mock.patch('app.main')
@mock.patch.dict(os.environ, {"FLASK_ENV": "testing"})
def test_main_in_testing_env(main_mock):
    app.main()
    main_mock.assert_called_once()

@mock.patch('app.main')
@mock.patch.dict(os.environ, {"FLASK_ENV": "production"})
def test_main_in_production_env(main_mock):
    app.main()
    main_mock.assert_called_once()
