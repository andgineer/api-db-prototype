import os

import db.conn
import db.models
import settings

SERVER_ENV = "SERVER_ENV"
TESTING_ENV = "testing"
DEV_ENV = "development"


app_env = os.environ.get(SERVER_ENV, "")
if app_env == TESTING_ENV:
    settings.config = settings.ConfigTest()
elif app_env == DEV_ENV:
    settings.config = settings.ConfigDev()
else:
    settings.config = settings.ConfigProd()

app = settings.config.app
db.conn.make_session()  # Connect to DB


def main() -> None:
    """Start http server."""
    assert settings.config
    settings.config.app.run(port=settings.config.port, debug=settings.config.debug_mode)


if __name__ == "__main__":
    main()
