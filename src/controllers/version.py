"""Version controller."""
from version import version


def get_version() -> str:
    """Returns app version."""
    return version()  # type: ignore
