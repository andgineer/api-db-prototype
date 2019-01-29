"""
Encapsulates SQLAlchemy engine, session and db management logic
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from sqlalchemy.orm import Session, scoped_session
from journaling import log
import settings
import db.models
import controllers.models
import settings
import alembic.config
import alembic.command
from sqlalchemy.engine import reflection


session: Session = None
engine = None


def create_admin_user():
    """
    Creates default admin if no users with admin right are in DB
    """
    # if session.info.get('has_flushed', False):
    users = db.models.User.query().filter(db.models.User.group == controllers.models.ADMIN_ACCESS_GROUP)
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
    global engine
    log.debug(f'...Connecting to DB {settings.config.db_uri}...')
    engine = create_engine(
        settings.config.db_uri,
        echo=settings.config.db_sqltrace
    )

    session = scoped_session(sessionmaker(bind=engine))  # ()
    Base.metadata.bind = engine
    if settings.config.db_autometa:
        refresh_metadata()
    create_admin_user()
    return session


def refresh_metadata():
    log.debug('Refreshing metadata...')
    insp = reflection.Inspector.from_engine(session().get_bind())
    table_names = insp.get_table_names()
    if 'users' not in table_names:
        log.info('Use alchemy to create meta DB')
        Base.metadata.create_all(session().get_bind())
    else:
        log.info('Use alembic to upgrade meta DB')

        # In fact settings.config is not None only for test
        alembic_root = 'src/' if isinstance(settings.config, settings.ConfigTest) else ''

        alembic_cfg = alembic.config.Config(f'{alembic_root}alembic.ini')
        alembic_cfg.set_main_option('script_location', f'{alembic_root}alembic')
        alembic_cfg.set_main_option('sqlalchemy.url', settings.config.db_uri)
        with session().get_bind().begin() as connection:
            alembic_cfg.attributes['connection'] = connection
            alembic.command.upgrade(alembic_cfg, 'head', sql=False)


