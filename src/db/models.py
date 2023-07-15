from typing import Any, Dict

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Table, event, func
from sqlalchemy.orm import attributes, declarative_base, relationship
from sqlalchemy.orm.base import NEVER_SET, NO_VALUE
from sqlalchemy.orm.query import Query

import db.conn
import password_hash
from controllers.models import APIError, UserGroup
from journaling import log


class ORMClass:
    """Base class for all ORM classes."""

    @classmethod
    def query(cls) -> Query[Any]:
        """Return query for this class."""
        return db.conn.session.query(cls)  # type: ignore  # mypy bug

    @classmethod
    def by_id(cls, id: str, check: bool = True) -> Any:
        """Find object by ID.

        If `check` then raise exception if not found.
        """
        result = cls.query().filter(cls.id == id).first()  # type: ignore  # we manually add id field to all models
        if not result:
            if check:
                raise APIError(f'There is no {cls.__name__} with id="{id}"')
            log.debug(f'{cls.__name__} with id="{id}" was not found')
        return result


Base = declarative_base(cls=ORMClass)


# Many-to-many relationship
projects_collaborators = Table(
    "projects_collaborators",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class Project(Base):  # type: ignore
    """Project model."""

    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False, comment="Project name")
    created = Column(
        DateTime(timezone=True),
        default=func.now(),  # pylint: disable=not-callable
        comment="Project creation time",
    )
    author_id = Column(Integer, ForeignKey("users.id"), comment="Project author")

    # we do not use 'backref' feature of SQLAlchemy but duplicate relationships
    # on both sides, because we want all this fields visible in auto-completion in IDE
    author = relationship(
        "User",
        foreign_keys=[author_id],
        back_populates="own_projects",
    )

    # all users that can see that project - author and who you add to it manually
    # author of the project added automatically
    collaborators = relationship(
        "User", secondary=projects_collaborators, back_populates="projects", lazy="dynamic"
    )

    def __repr__(self) -> str:
        """Return string representation of the object."""
        return f"name: {self.name}, id: {self.id}"


class User(Base):  # type: ignore
    """User model."""

    __tablename__ = "users"
    createdDatetime = Column(
        "created_datetime",
        DateTime(timezone=True),
        default=func.now(),  # pylint: disable=not-callable
    )
    name = Column(String(120), comment="User name")
    id = Column(Integer, primary_key=True)
    group = Column(  # type: ignore
        Enum(
            UserGroup,
            values_callable=lambda x: [e.value for e in x],  # to use enum values instead of names
            native_enum=False,
        ),
        comment="User group",
    )
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(300))

    # all projects that this user can see - his own and where he added to collaborators
    own_projects = relationship("Project", back_populates="author", lazy="dynamic")
    projects = relationship(
        "Project", back_populates="collaborators", secondary=projects_collaborators, lazy="dynamic"
    )

    @property
    def password(self) -> str:
        """Password getter."""
        raise NotImplementedError("Password getter")

    @password.setter
    def password(self, value: str) -> None:
        """For hybrid_property in setter we should check.

        not isinstance(self._scaffold_smiles, sqlalchemy.orm.attributes.InstrumentedAttribute)
        """
        self.password_hash = password_hash.hash(value)  # type: ignore

    @staticmethod
    def by_email(email: str, check: bool = True) -> "User":
        """Find user by email.

        If `check` then raise exception if not found.
        """
        user = User.query().filter(func.lower(db.models.User.email) == email.lower()).first()
        if not user:
            if check:
                raise APIError(f'There is no user with email "{email}"')
            log.debug(f'User with email "{email}" was not found')
        return user  # type: ignore

    @property
    def as_dict(self) -> Dict[str, Any]:
        """Return dict representation of the object."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        """Return string representation of the object."""
        return f"name: {self.name}, email: {self.email}, id: {self.id}"


@event.listens_for(Project.author, "set")
def project_author_set_listener(
    project: Project,
    author: User,
    old_author: User,
    initiator: attributes.Event,  # pylint: disable=unused-argument
) -> None:
    """Listen for Project.author set event."""
    author.projects.append(project)
    if old_author not in [NEVER_SET, NO_VALUE]:
        old_author.projects.remove(project)
    log.debug(
        f'{author.email}\'s own project "{project.name}" added also to her full list of projects'
    )
