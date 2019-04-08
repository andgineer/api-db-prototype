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
from typing import Optional
from pretty_ns import time_ns
import settings


LOG_CONFIG = 'logging.yaml'
hostname = None  # host name for the machine we are running on
user = None  # user email for the token used to call api request (if any)
log = logging.getLogger('')  # convenient way to get logger
request_start_time: int = None  # time_ns before starting request handler, set in controllers/request#api_result handler


def uwsgi_info() -> Optional[dict]:
    try:
        import uwsgi
        return {
            'numproc': uwsgi.numproc,
            'worker_id': uwsgi.worker_id(),
            'workers': uwsgi.workers()
        }
    except ImportError:  # we are not under uWSGI
        return {
            'numproc': 0,
            'worker_id': 'N/A',
            'workers': []
        }


def elapsed() -> str:
    if request_start_time is None:
        return '|n/a|'
    ms = (time_ns() - request_start_time) / 1000000
    if ms > settings.config.profiler_maxMs:
        return f'**>{ms:.0f}ms<**'
    else:
        return f'*>{ms:.1f}ms<*'


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'host'):
            record.host = hostname
        if not hasattr(record, 'uwsgi'):
            record.uwsgi = uwsgi_info()['worker_id']
        record.user = user
        record.elapsed = elapsed()
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

