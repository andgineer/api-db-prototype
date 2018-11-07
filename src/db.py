import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models


db_name = '../test.sqlite'
engine_connection_string = 'sqlite:///' + db_name

engine = create_engine(engine_connection_string)

session = sessionmaker(bind=engine)()
#session.configure(bind=engine)

models.Base.metadata.bind = engine


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.sqlite'
# db = SQLAlchemy(app)
