"""Version controller."""
from version import version  # type: ignore


def get_version() -> str:
    """Returns app version."""
    return version()  # type: ignore
