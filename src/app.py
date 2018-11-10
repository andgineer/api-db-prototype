from swagger_server.api_app import app
#from transmute_server.api_app import app
from config import ConfigDev
import db.conn
import db.models
import controllers.db


def main():
    config = ConfigDev()
    controllers.db.session = db.conn.make_session(config)
    controllers.db.models = db.models
    app.run(port=config.port)


if __name__ == '__main__':
    main()
