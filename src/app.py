"""
Transmute version of app
API should be described in code and the app can auto-generate Open API (swagger) UI from the code.
"""
# import sys
# import os
# PACKAGE_PARENT = '..'
# SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
# sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from db.db import db
from config import ConfigDev
import connexion
from swagger_server import encoder

app = connexion.App(__name__, specification_dir='./swagger_server/swagger')
app.json_encoder = encoder.JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'compbiowebAPI'})

def main():
    config=ConfigDev()
    db.connect(config)

    app.run(port=config.port)


if __name__ == '__main__':
    main()
