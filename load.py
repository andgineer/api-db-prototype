import os
import requests
import json
import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


setup_logging()
log = logging.getLogger('')


class LoadTest(object):
    def __init__(self, gun):
        self.gun = gun
        self.api_host = self.gun.get_option("base_address", "")

    def get(self, missile):
        with self.gun.measure("Get users list"):
            result = requests.get(
                self.api_host + '/users',
                json={'page': '1', 'per_page': '30'},
                headers={'Authorization': 'Bearer ' + self.token}
            )
            #log.debug('Users list reply: '+result.text)
            users = json.loads(result.text)

        with self.gun.measure("Get user") as sample:
            result = requests.get(
                self.api_host + '/users/' + users[0]['id'],
                headers={'Authorization': 'Bearer ' + self.token}
            )
            #log.debug('User reply: '+result.text)

    def crud(self, missile):
        with self.gun.measure("CRUD"):
            result = requests.get(
                self.api_host + '/users',
                json={'page': '1', 'per_page': '30'},
                headers={'Authorization': 'Bearer ' + self.token}
            )
            #log.debug('Users list reply: '+result.text)
            users = json.loads(result.text)

        with self.gun.measure("Get user") as sample:
            result = requests.get(
                self.api_host + '/users/' + users[0]['id'],
                headers={'Authorization': 'Bearer ' + self.token}
            )
            #log.debug('User reply: '+result.text)

    def awt(self, missile):
        with self.gun.measure("AWT"):
            result = requests.post(
                self.api_host + '/auth',
                json={'email': 'admin@', 'password': 'admin'},
            )

    def default(self, missile):
        with self.gun.measure("default"):
            log.info("Shoot default: %s", missile)

    def setup(self, param):
        """
        this will be executed in each worker before the test starts
        """
        #log.info("Get token")
        result = requests.post(
            self.api_host + '/auth',
            json={'email': 'admin@', 'password': 'admin'},
        )
        #log.debug('Get from auth: ' + result.text)
        self.token = json.loads(result.text)['token']
        #log.debug(self.token)

    def teardown(self):
        """
        this will be executed in each worker after the end of the test
        """
        #log.info("Tearing down LoadTest")
        #It's mandatory to explicitly stop worker process in teardown
        os._exit(0)
        return 0
