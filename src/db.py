from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models


class DB():
    file_name = '../test.sqlite'
    driver_name = 'sqlite:///'
    user = None
    password = None

    def open(self):
        user_str = f'{user}:{password}@' if self.user else ''
        self.uri = f'{self.driver_name}{user_str}{self.file_name}'
        self.engine = create_engine(self.uri)
        self.session = sessionmaker(bind=self.engine)()
        models.Base.metadata.bind = self.engine
        self.create_meta()

    def create_meta(self):
        models.Base.metadata.create_all(self.engine)
        self.session.commit()


db = DB()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.sqlite'
# db = SQLAlchemy(app)
