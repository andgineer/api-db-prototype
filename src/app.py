from config import ConfigDev
import db.conn
import db.models


def main():
    config = ConfigDev()

    db.conn.make_session(config)

    # Starting http server
    config.app.run(port=config.port)


if __name__ == '__main__':
    main()
