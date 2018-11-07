import models
import db

print(f'Creating DB at (db.engine_connection_string)...')
models.Base.metadata.create_all(db.engine)
db.session.commit()
print(f'Done!')
