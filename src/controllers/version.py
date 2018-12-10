from version import version
from flask import make_response


def get_version():
    """
    Returns app version
    """
    return version()
