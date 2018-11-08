import os
from abc import abstractmethod
import tempfile


class ConfigBase():
    db_file_name = None
    db_driver_name = None
    db_user = None
    db_password = None

    _port=5000

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
            print(f'...Connecting to DB {uri}...')
            return uri
        else:
            raise Exception('No DB parameters specified.')

    @property
    def port(self):
        return self._port  #todo: use env if defined


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


class ConfigDev(ConfigBase):
    """
    Development environment.
    Local sqlite DB.
    """
    def __init__(self):
        super().__init__()
        self.db_file_name = '../test.sqlite'
        self.db_driver_name = 'sqlite:///'


class ConfigProd(ConfigBase):
    """
    Production.
    """
    def __init__(self):
        super().__init__()
        #self.db_file_name = ''
        #self.db_driver_name = ':////'
