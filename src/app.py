from swagger_server.api_app import app
#from transmute_server.api_app import app
from config import ConfigDev
import db.conn
import db.models


def main():
    config = ConfigDev()

    db.conn.make_session(config)

    # Starting http server
    app.run(port=config.port)


if __name__ == '__main__':
    main()
