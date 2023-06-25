"""
Returns version as 'build' time from file build_timestamp
See add_commit_date_git_hook.sh and hook_install.sh
"""


def version():
    try:
        return open("build_timestamp", "r").read().strip()
    except Exception:
        return None


if __name__ == "__main__":
    print(version())
