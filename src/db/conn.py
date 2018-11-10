"""
Encapsulates SQLAlchemy engine, session and db management logic
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from sqlalchemy.orm import Session


session: Session = None


def make_session(config):
    global session
    print(f'...Connecting to DB {config.db_uri}...')
    engine = create_engine(config.db_uri)
    session = sessionmaker(bind=engine)()
    Base.metadata.bind = engine
    return session


def refresh_metadata():
    Base.metadata.create_all(session.get_bind())
    session.commit()
