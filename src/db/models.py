from sqlalchemy import Table, Column, DateTime, String, Integer, ForeignKey, func, event
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import passwords
from sqlalchemy.orm import attributes
from journaling import log


Base = declarative_base()


# Many-to-many relationship
projects_collaborators = Table(
    'projects_collaborators',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
)


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    created = Column(DateTime(timezone=True), default=func.now())
    author_id = Column(Integer, ForeignKey('users.id'))

    # we do not use 'backref' feature of SQLAlchemy but duplicate relationships
    # on both sides, because we want all this fields visible in auto-completion in IDE
    author = relationship(
        'User',
        foreign_keys=[author_id],
        back_populates='own_projects',
    )

    # all users that can see that project - author and who you add to it manually
    # author of the project added automatically
    collaborators = relationship(
        'User',
        secondary=projects_collaborators,
        back_populates='projects',
        lazy='dynamic'
    )

    def __repr__(self):
        return f'name: {self.name}, id: {self.id}'


class User(Base):
    __tablename__ = 'users'
    name = Column(String(120))
    id = Column(Integer, primary_key=True)
    group = Column(String(32))
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(300))

    # all projects that this user can see - his own and where he added to collaborators
    own_projects = relationship('Project', back_populates='author', lazy='dynamic')
    projects = relationship(
        'Project',
        back_populates='collaborators',
        secondary=projects_collaborators,
        lazy='dynamic'
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


@event.listens_for(Project.author, 'set')
def project_author_set_listener(project: Project, author: User, old_author: User, initiator: attributes.Event):
    author.projects.append(project)
    if old_author:
        old_author.projects.remove(project)
    log.debug(f'{author.email}\'s own project "{project.name}" added also to her full list of projects')