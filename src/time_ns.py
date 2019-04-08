try:
    from time import time_ns
except ImportError:
    from time import perf_counter


    def time_ns():
        return perf_counter() * 10 ** 9
