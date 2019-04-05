import cProfile
from io import StringIO
import pstats
import contextlib
from src import settings
import logging


log = logging.getLogger()


@contextlib.contextmanager
def analyze():
    if settings.config.profiler_cprofile:
        pr = cProfile.Profile()
        pr.enable()
    yield
    if settings.config.profiler_cprofile:
        pr.disable()
        s = StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        # uncomment this to see who's calling what
        # ps.print_callers()
        log.debug('=-=profile=-=:'*10 + s.getvalue())