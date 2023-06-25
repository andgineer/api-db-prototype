import datetime
from datetime import timezone

import pytest

import db.models
import settings
from conftest import DEFAULT_USERS


def db_date():
    """
    Date in DB ORM format
    """
    return datetime.datetime.now()


@pytest.fixture(scope="session")
def db_users():
    """
    List of user's dicts in DB ORM format
    """
    return [
        {"name": "Cathy", "email": "cathy@", "group": "guest", "password": "12345"},
        {"name": "Marry", "email": "marry@", "group": "guest", "password": "12345"},
        {"name": "John", "email": "john@", "group": "guest", "password": "12345"},
    ]


@pytest.fixture(scope="session")
def db_projects():
    """
    List of projects's names in DB ORM format
    """
    return [{"name": "IT"}, {"name": "Financial"}, {"name": "Failed"}]


def test_wrong_config(wrong_session):
    pass


def test_rfc3339():
    time = datetime.datetime.now(timezone.utc)
    date = time.replace(hour=0, minute=0, second=0, microsecond=0)
    assert settings.config.rfc3339_to_date(settings.config.date_to_rfc3339(time)) == date


def test_db(session, db_users, db_projects):
    user_objects = []
    for user_dict in db_users:
        user = db.models.User(**user_dict)
        session.add(user)
        user_objects.append(user)

    projects_objects = []
    user0_projects_names = []
    for project_dict in db_projects:
        project = db.models.Project(**project_dict)
        session.add(project)
        project.author = user_objects[0]
        projects_objects.append(project)
        user0_projects_names.append(project.name)

    assert session.query(db.models.User).count() == len(db_users) + DEFAULT_USERS

    user0_projects = (
        session.query(db.models.User).filter_by(email=user_objects[0].email).first().projects
    )
    assert len(user0_projects.all()) == len(db_projects)  # first user uwns all the projects
    assert user0_projects[0].name in user0_projects_names
