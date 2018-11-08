from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models


class DB():
    def connect(self, config):
        self.engine = create_engine(config.db_uri)
        self.session = sessionmaker(bind=self.engine)()
        models.Base.metadata.bind = self.engine

    def create_meta(self):
        models.Base.metadata.create_all(self.engine)
        self.session.commit()


db = DB()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.sqlite'
# db = SQLAlchemy(app)
