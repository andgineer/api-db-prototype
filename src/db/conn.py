"""
Encapsulates SQLAlchemy engine, session and db management logic
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from sqlalchemy.orm import Session
from journaling import log
import settings
import db.models
import controllers.models
import datetime
import settings
#from sqlalchemy import event


session: Session = None


# @event.listens_for(Session, "after_flush")
# def log_transaction(session, flush_context):
#     """
#     We want to know if metadata was created so we have to create default admin
#     """
#     session.info['has_flushed'] = True


def create_admin_user():
    """
    Creates default admin if no users with admin right are in DB
    """
    # if session.info.get('has_flushed', False):
    users = session.query(db.models.User).filter(db.models.User.group == controllers.models.ADMIN_ACCESS_GROUP)
    if not users.count():
        log.debug('!' * 25 + f"""
Creating default admin user <{settings.config.default_admin_email}> with
password '{settings.config.default_admin_password}' - please change her password
""" + '!' * 25)
        admin_user = db.models.User(
            email=settings.config.default_admin_email,
            password=settings.config.default_admin_password,
            group=controllers.models.ADMIN_ACCESS_GROUP
        )
        session.add(admin_user)
        session.commit()
    else:
        log.debug(f'In db found users with admin roles: {", ".join([user.email for user in users])}')


def make_session():
    global session
    log.debug(f'...Connecting to DB {settings.config.db_uri}...')
    engine = create_engine(settings.config.db_uri)
    session = sessionmaker(bind=engine)()
    Base.metadata.bind = engine
    if settings.config.auto_db_meta:
        refresh_metadata()
    create_admin_user()
    return session


def refresh_metadata():
    log.debug('Refreshing metadata...')
    Base.metadata.create_all(session.get_bind())
    session.commit()
