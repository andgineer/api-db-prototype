"""Return version as 'build' time from file build_timestamp.

See add_commit_date_git_hook.sh and hook_install.sh
"""

from typing import Optional


def version() -> Optional[str]:
    """Return app version."""
    try:
        return open("build_timestamp", encoding="utf8").read().strip()
    except Exception:
        return None


if __name__ == "__main__":
    print(version())
