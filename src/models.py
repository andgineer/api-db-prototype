from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from db import db


Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    created = Column(DateTime, default=func.now())
    users = relationship(
        'User',
        secondary='project_user_link',
        backref=backref('project_user_link_backref', lazy='dynamic')
    )

    def __repr__(self):
        return f'name: {self.name}, id: {self.id}'


class User(Base):
    __tablename__ = 'project_users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created = Column(DateTime, default=func.now())
    projects = relationship(
        'Project',
        secondary='project_user_link',
        backref=backref('project_user_link_backref', lazy='dynamic')
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if
                not isinstance(getattr(self, c.name), datetime)}

    def __repr__(self):
        return f'name: {self.name}, email: {self.email}, id: {self.id}'


class ProjectUserLink(Base):
    __tablename__ = 'project_user_link'
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('project_users.id'), primary_key=True)
