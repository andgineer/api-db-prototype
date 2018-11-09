import db.models
import db.db

print(f'Creating DB at (db.engine_connection_string)...')
db.models.Base.metadata.create_all(db.db.engine)
db.db.session.commit()
print(f'Done!')
