import contextlib
import cProfile
import logging
import pstats
from collections.abc import Generator
from io import StringIO

from src import settings

log = logging.getLogger()


@contextlib.contextmanager
def analyze() -> Generator[None, None, None]:
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
