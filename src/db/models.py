from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import passwords
from datetime import datetime, timezone
import settings


Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    created = Column(DateTime(timezone=True), default=func.now())
    users = relationship(
        'User',
        secondary='project_user_link',
        backref=backref('project_user_link_backref', lazy='dynamic')
    )

    def __repr__(self):
        return f'name: {self.name}, id: {self.id}'


class User(Base):
    __tablename__ = 'project_users'
    name = Column(String(120))
    id = Column(Integer, primary_key=True)
    group = Column(String(32))
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(300))
    projects = relationship(
        'Project',
        secondary='project_user_link',
        backref=backref('project_user_link_backref', lazy='dynamic')
    )

    @property
    def password(self):
        raise Exception('Password getter')

    @password.setter
    def password(self, value):
        self.password_hash = passwords.hash(value)

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'name: {self.name}, email: {self.email}, id: {self.id}'


class ProjectUserLink(Base):
    __tablename__ = 'project_user_link'
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('project_users.id'), primary_key=True)
