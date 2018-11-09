from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base


class DB:
    def connect(self, config):
        self.engine = create_engine(config.db_uri)
        self.session = sessionmaker(bind=self.engine)()
        Base.metadata.bind = self.engine

    def create_meta(self):
        Base.metadata.create_all(self.engine)
        self.session.commit()


db = DB()


