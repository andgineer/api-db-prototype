import models
from db import db


def test_db(empty_db, users, projects):
    projects_objects = []
    for project_dict in projects:
        projects_objects.append(models.Project(**project_dict))
        db.session.add(projects_objects[-1])

    cathy = models.User(name='Cathy', email='cathy@')
    marry = models.User(name='Marry', email='marry@')
    john = models.User(name='John', email='john@')
    db.session.add(cathy)
    db.session.add(marry)
    db.session.add(john)

    cathy.projects.append(projects_objects[0])
    marry.projects.append(projects_objects[1])

    john_projects_names = []
    for project in projects_objects[:-1]:
        john.projects.append(project)
        john_projects_names.append(project.name)

    assert db.session.query(models.User).count() == len(users)

    john_projects = db.session.query(models.User).filter_by(name=john.name).first().projects
    assert len(john_projects) == len(projects) - 1
    assert john_projects[0].name in john_projects_names



