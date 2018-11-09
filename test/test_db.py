from db import models
from db.db import db


def test_db(empty_db, users, projects):
    projects_objects = []
    for project_dict in projects:
        project = models.Project(**project_dict)
        projects_objects.append(project)
        db.session.add(project)

    user_objects = []
    for user_dict in users:
        user = models.User(**user_dict)
        user_objects.append(user)
        db.session.add(user)

    user0_projects_names = []
    for project in projects_objects[:-1]:
        user_objects[0].projects.append(project)
        user0_projects_names.append(project.name)

    assert db.session.query(models.User).count() == len(users)

    user0_projects = db.session.query(models.User).filter_by(name=user_objects[0].name).first().projects
    assert len(user0_projects) == len(projects) - 1
    assert user0_projects[0].name in user0_projects_names
