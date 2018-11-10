"""
Encapsulates SQLAlchemy engine, session and db management logic
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base


def make_session(config):
    print(f'...Connecting to DB {config.db_uri}...')
    engine = create_engine(config.db_uri)
    session = sessionmaker(bind=engine)()
    Base.metadata.bind = engine
    return session


def refresh_metadata(session):
    Base.metadata.create_all(session.get_bind())
    session.commit()
