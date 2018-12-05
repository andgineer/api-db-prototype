import os
from abc import abstractmethod
import tempfile
import datetime
from flask_server.api_app import app as flask_app
#from transmute_server.api_app import app as transmute_app
#from swagger_server.api_app import app as connexion_app
from datetime import timezone
import urllib


# environment vars
DB_URI_ENV = 'DB_URI'  # env var for DB URI (see ConfigBase.db_uri)
PORT_ENV = 'API_PORT'  # env var for app port, default in DEFAULT_PORT
AUTO_DB_META_ENV = 'AUTO_DB_META'  # env var, if 1 then server at start
# refresh DB metadata (create tables if necessary)

# const used for prod config
DEFAULT_PORT = 5000
TOKEN_EXPIRATION_HOURS = 48  # jwt lifetime
DEFAULT_ADMIN_EMAIL = 'admin@'
DEFAULT_ADMIN_PASSWORD = 'admin'
PRIVATE_JWT_KEY_FILE = 'secret/jwt_private.key'
PUBLIC_JWT_KEY_FILE = 'secret/jwt_certificate.pem'


class ConfigBase:
    jwt_secret_key_file = None
    jwt_public_key_file = None

    token_expiration_delta = datetime.timedelta(hours=TOKEN_EXPIRATION_HOURS)

    default_admin_email = DEFAULT_ADMIN_EMAIL
    default_admin_password = DEFAULT_ADMIN_PASSWORD

    _port = DEFAULT_PORT
    _db_uri = None

    db_autometa = True  # refresh DB metadata at start
    db_sqltrace = False

    api_host = None
    api_root = ''

    @property
    def api_url(self):
        return urllib.parse.urljoin(self.api_host, self.api_root)

    @property
    @abstractmethod
    def app(self):
        """
        Flask-compatible App server to run.
        """
        pass

    @property
    def db_uri(self):
        """
        DB URI: engine://user:password@path.
        For example:
            postgres://user@example.com/template1
            sqlite:////data/test.sqlite
        """
        if self._db_uri:
            return self._db_uri
        else:
            raise ValueError(f'No DB URI specified')

    @db_uri.setter
    def db_uri(self, value):
        self._db_uri = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @staticmethod
    def now():
        """
        To have one place to decide whether we use utc or server timezone.
        And for ease of mocking in expiration tests.
        """
        return datetime.datetime.now(timezone.utc)

    def from_date_str(self, date_str: str) -> datetime:
        """
        Converts date string into datetime
        """
        return self.rfc3339_to_date(date_str)

    @staticmethod
    def date_to_rfc3339(date: datetime) -> str:
        """
        Date as 'yyyy-mm-dd'
        """
        return date.isoformat(sep='T').split('T')[0]

    @staticmethod
    def rfc3339_to_date(date_str: str) -> datetime:
        """
        'yyyy-mm-dd' (UTC) to datetime
        """
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)


class ConfigTest(ConfigBase):
    """
    Creates temp sqlite db.
    """
    def __init__(self):
        super().__init__()
        self.db_file_object, self.db_file_name = tempfile.mkstemp()
        self.db_uri = 'sqlite:///' + self.db_file_name
        self.jwt_public_key_file = 'src/secret/jwt_certificate.pem'
        self.jwt_secret_key_file = 'src/secret/jwt_private.key'
        self.api_host = 'http://localhost:5000'

    def __del__(self):
        os.close(self.db_file_object)
        os.remove(self.db_file_name)


class ConfigTestPureFlask(ConfigTest):
    """
    Creates temp sqlite db.
    """
    @property
    def app(self):
        return flask_app


# class ConfigTestTransmute(ConfigTest):
#     """
#     Creates temp sqlite db.
#     """
#     @property
#     def app(self):
#         return transmute_app
#
#
# class ConfigTestConnexion(ConfigTest):
#     """
#     Creates temp sqlite db.
#     """
#     @property
#     def app(self):
#         return connexion_app


class ConfigDev(ConfigBase):
    """
    Development environment.
    Local sqlite DB.
    """
    def __init__(self):
        super().__init__()
        self.db_uri = 'sqlite:///../debug_db.sqlite'
        self.jwt_public_key_file = 'secret/jwt_certificate.pem'
        self.jwt_secret_key_file = 'secret/jwt_private.key'

    @property
    def app(self):
        return flask_app


class ConfigProd(ConfigBase):
    """
    Production.
    """
    def __init__(self):
        super().__init__()
        self.db_uri = os.environ.get(DB_URI_ENV, None)
        self.port = os.environ.get(PORT_ENV, self.port)
        self.auto_db_meta = int(os.environ.get(AUTO_DB_META_ENV, 0))
        self.jwt_public_key_file = PUBLIC_JWT_KEY_FILE
        self.jwt_secret_key_file = PRIVATE_JWT_KEY_FILE
        self.api_host = 'https://example.com'

    @property
    def app(self):
        return flask_app


class ConfigTestWrong(ConfigBase):
    """
    To test wrong config
    """

    @property
    def app(self):
        return flask_app


config: ConfigBase = None  # Convenient config injection
# app is responsible to populate this var with config object
