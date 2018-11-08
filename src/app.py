from api import app
from db import db
from config import ConfigDev


config=ConfigDev()
db.connect(config)
app.run(port=config.port)
