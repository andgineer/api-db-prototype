"""Logger with custom fields like hostname.

Convenient way of use:
    from journaling import log
    log.debug('hey!')

Before first use you have to initialize it:
    import journaling
    journaling.setup('my_log_config.yaml')
"""

import logging
import logging.config
import os
import socket
from typing import Any, Dict, Optional

import yaml

from pretty_ns import time_ns

LOG_CONFIG = "logging.yaml"
PROFILER_MAXMS = 1000  # max time in ms to log profiler results
hostname: Optional[str] = None  # host name for the machine we are running on
user: Optional[str] = None  # user email for the token used to call api request (if any)
log = logging.getLogger("")  # convenient way to get logger
request_start_time: Optional[int] = (
    None  # time_ns before starting request handler, set in controllers/request#api_result handler
)


def uwsgi_info() -> Dict[str, Any]:
    """Get uWSGI info if we are under uWSGI."""
    try:
        import uwsgi

        return {
            "numproc": uwsgi.numproc,
            "worker_id": uwsgi.worker_id(),
            "workers": uwsgi.workers(),
        }
    except ImportError:  # we are not under uWSGI
        return {"numproc": 0, "worker_id": "N/A", "workers": []}


def elapsed() -> str:
    """Return elapsed time since request start in ms."""
    if request_start_time is None:
        return "|n/a|"
    ms = (time_ns() - request_start_time) / 1000000
    return f"**>{ms:.0f}ms<**" if ms > PROFILER_MAXMS else f"*>{ms:.1f}ms<*"


class CustomFormatter(logging.Formatter):
    """Custom formatter for logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Add custom fields to log record."""
        if not hasattr(record, "host"):
            record.host = hostname
        if not hasattr(record, "uwsgi"):
            record.uwsgi = uwsgi_info()["worker_id"]
        record.user = user
        record.elapsed = elapsed()
        return super().format(record)


def setup(log_config: Optional[str] = LOG_CONFIG, default_level: int = logging.DEBUG) -> None:
    """Set logging configuration and returns logger."""
    global hostname  # pylint: disable=global-statement
    if log_config is None:
        log_config = LOG_CONFIG
    if os.path.exists(log_config):
        with open(log_config, "r", encoding="utf8") as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    else:
        config = None
        logging.basicConfig(level=default_level, datefmt="%m.%d %H:%M:%S")

    hostname = socket.gethostname()

    handler = logging.StreamHandler()
    handler.setFormatter(
        CustomFormatter(
            "[%(asctime)s] <%(filename)s:%(lineno)d> {host=%(host)s} %(levelname)s - %(message)s"
        )
    )
    log.addHandler(handler)

    if config is not None:
        log.info(
            f'Logging settings were loaded from {log_config}\nHandlers: {config["root"]["handlers"]}'
        )


if __name__ == "__main__":
    setup("debug/logging.yaml")
    log.error("hey!", extra={"host": "redefined host"})
    log.error("hey!")
