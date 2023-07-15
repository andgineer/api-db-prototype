import contextlib
import cProfile
import logging
import pstats
from io import StringIO

from src import settings

log = logging.getLogger()


@contextlib.contextmanager  # type: ignore
def analyze():  # type: ignore
    """Analyze."""
    if settings.config.profiler_cprofile:
        pr = cProfile.Profile()
        pr.enable()
    yield
    if settings.config.profiler_cprofile:
        pr.disable()
        s = StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
        ps.print_stats()
        # uncomment this to see who's calling what
        # ps.print_callers()
        log.debug("=-=profile=-=:" * 10 + s.getvalue())  # pylint: disable=logging-not-lazy
