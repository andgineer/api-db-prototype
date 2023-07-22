"""Version controller."""
from controllers.models import HttpCode
from version import version


def get_version() -> str:
    """Return app version."""
    result = version()
    if result is None:
        return "Version undefined", HttpCode.logic_error  # type: ignore
    return result
