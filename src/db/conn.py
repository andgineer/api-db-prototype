"""Encapsulate SQLAlchemy engine, session and db management logic."""

from typing import Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.orm import Session, scoped_session, sessionmaker

import alembic.command
import alembic.config
import controllers.models
import db.models
import settings
from db.models import Base
from journaling import log

session: Optional[Session] = None  # todo we mixed Session and Session() in code
engine: Optional[Engine] = None


def create_admin_user() -> None:
    """Create default admin if no users with admin right are in DB."""
    assert session is not None, "First init session with make_session()"
    assert settings.config
    # if session.info.get('has_flushed', False):
    users = db.models.User.query().filter(
        db.models.User.group == controllers.models.UserGroup.ADMIN,
    )
    if not users.count():
        log.debug(  # pylint: disable=logging-not-lazy
            "!" * 25
            + f"""
Creating default admin user <{settings.config.default_admin_email}> with
password '{settings.config.default_admin_password}' - please change her password
"""
            + "!" * 25,
        )
        admin_user = db.models.User(
            email=settings.config.default_admin_email,
            password=settings.config.default_admin_password,
            group=controllers.models.UserGroup.ADMIN,
        )
        session.add(admin_user)
        session.commit()
    else:
        log.debug(
            f"In db found users with admin roles: {', '.join([user.email for user in users])}",
        )


def make_session() -> Session:
    """Make session."""
    global session  # pylint: disable=global-statement
    global engine  # pylint: disable=global-statement
    assert settings.config
    log.debug(f"...Connecting to DB {settings.config.db_uri}...")
    engine = create_engine(settings.config.db_uri, echo=settings.config.db_sqltrace)

    session = scoped_session(sessionmaker(bind=engine))  # type: ignore  # ()
    Base.metadata.bind = engine
    if settings.config.db_autometa:
        refresh_metadata()
    create_admin_user()
    session.close()  # type: ignore
    session.get_bind().dispose()  # type: ignore
    log.debug("Connections dropped after creating meta-data")
    return session  # type: ignore


def refresh_metadata() -> None:
    """Refresh metadata."""
    # todo here we expect callable session
    log.debug("Refreshing metadata...")
    assert session is not None
    assert settings.config
    insp = reflection.Inspector.from_engine(session().get_bind())  # type: ignore
    table_names = insp.get_table_names()
    if "users" not in table_names:
        log.info("Use alchemy to create meta DB")
        Base.metadata.create_all(session().get_bind())  # type: ignore
    else:
        log.info("Use alembic to upgrade meta DB")

        # In fact settings.config is not None only for test
        alembic_root = "src/" if isinstance(settings.config, settings.ConfigTest) else ""

        alembic_cfg = alembic.config.Config(f"{alembic_root}alembic.ini")
        alembic_cfg.set_main_option("script_location", f"{alembic_root}alembic")
        alembic_cfg.set_main_option("sqlalchemy.url", settings.config.db_uri)
        with session().get_bind().begin() as connection:  # type: ignore
            alembic_cfg.attributes["connection"] = connection
            alembic.command.upgrade(alembic_cfg, "head", sql=False)
