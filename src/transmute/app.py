"""
Transmute version of app
API should be described in code and the app can auto-generate Open API (swagger) UI from the code.
"""
from transmute.api import app
from db.db import db
from config import ConfigDev


config=ConfigDev()
db.connect(config)
app.run(port=config.port)
