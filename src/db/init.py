import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import db.conn
from config import ConfigDev


config = ConfigDev()
print(f'Refreshing metadata in ({config.db_uri})...')
db.conn.make_session(config)
db.conn.refresh_metadata()
print(f'Done!')
