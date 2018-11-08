from create_app import app
from db import db

db.open()
app.run()
