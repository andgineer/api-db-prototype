import os
from abc import abstractmethod
import tempfile
from flask_server.api_app import app as flask_app
from transmute_server.api_app import app as transmute_app
from swagger_server.api_app import app as swagger_app


class ConfigBase():
    db_file_name = None
    db_driver_name = None
    db_user = None
    db_password = None

    _port = 5000

    @abstractmethod
    def __init__(self):
        """
        Descendants have to fill attributes listed above.
        """
        pass

    @property
    def db_uri(self):
        """
        :return: DB connection string composed from the config atributes .
        """
        user_str = f'{self.db_user}:{self.db_password}@' if self.db_user else ''
        if self.db_driver_name and self.db_file_name:
            uri = f'{self.db_driver_name}{user_str}{self.db_file_name}'
            return uri
        else:
            raise ValueError(f'No DB parameters specified: driver="{self.db_driver_name}", file="{self.db_file_name}"')

    @property
    def port(self):
        return self._port  #todo: use env if defined

    #@abstractmethod
    @property
    def app(self):
        pass


class ConfigTest(ConfigBase):
    """
    Creates temp sqlite db.
    """
    def __init__(self):
        super().__init__()
        self.db_driver_name = 'sqlite:///'
        self.db_file_object, self.db_file_name = tempfile.mkstemp()

    def __del__(self):
        os.close(self.db_file_object)
        os.remove(self.db_file_name)


class ConfigTestTransmute(ConfigTest):
    """
    To test transmute server
    """
    @property
    def app(self):
        return transmute_app


class ConfigTestSwagger(ConfigTest):
    """
    To test swagger server
    """
    @property
    def app(self):
        return swagger_app


class ConfigTestFlask(ConfigTest):
    """
    To test flask server
    """
    @property
    def app(self):
        return flask_app


class ConfigDev(ConfigBase):
    """
    Development environment.
    Local sqlite DB.
    """
    def __init__(self):
        super().__init__()
        self.db_file_name = '../test.sqlite'
        self.db_driver_name = 'sqlite:///'

    @property
    def app(self):
        return flask_app


class ConfigProd(ConfigBase):
    """
    Production.
    """
    def __init__(self):
        super().__init__()
        #self.db_file_name = ''
        #self.db_driver_name = ':////'

    @property
    def app(self):
        return flask_app


class ConfigTestWrong(ConfigBase):
    """
    To test wrong config
    """
    def __init__(self):
        super().__init__()

    @property
    def app(self):
        return flask_app
