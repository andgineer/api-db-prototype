"""
Logger with custom fields like hostname.
Convenient way of use:
    from journaling import log
    log.debug('hey!')

Before first use you have to initialize it:
    import journaling
    journaling.setup('my_log_config.yaml')
"""
import logging
import os
import logging.config
import yaml
import socket


LOG_CONFIG = 'logging.yaml'
hostname = None  # host name for the machine we are running on
log = logging.getLogger('')  # convenient way to get logger


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'host'):
            record.host = hostname
        return super().format(record)


def setup(log_config=LOG_CONFIG, default_level=logging.DEBUG):
    """
    Setup logging configuration and returns logger
    """
    global hostname
    if os.path.exists(log_config):
        with open(log_config, 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    else:
        config = None
        logging.basicConfig(
            level=default_level,
            datefmt='%m.%d %H:%M:%S'
        )

    hostname = socket.gethostname()

    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter('[%(asctime)s] <%(filename)s:%(lineno)d> {host=%(host)s} %(levelname)s - %(message)s'))
    log.addHandler(handler)

    if config is not None:
        log.info(f'Logging settings were loaded from {log_config}\nHandlers: {config["root"]["handlers"]}')


if __name__ == '__main__':
    setup('../logging.yaml')
    log.error('hey!', extra={'host': 'redefined host'})
    log.error('hey!')

