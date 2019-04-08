"""
- time_ns for Python before 3.7
- Elapsed context manager
- pretty_ns to represent time elapsed in human lovable form

Usage:
>>> start = time_ns()
>>> pass  # code to time
>>> pretty_ns((start + 100) - start)
'0.1 mks'

>>> with Timer() as timer:
...     pass
...     timer.pretty.endswith('s')
...     timer.ns > 0
True
True

"""

time_ns = None  # for Python3.7+ this is function from system library time
# for earlier Python versions this is emulation of the Python3.7 time_ns


def pretty_ns(elapsed_ns: int):
    dividers = {
        'us': 1,
        'mks': 1000,
        'ms': 1000,
        's': 1000,
        'minutes': 60,
        'hours': 60,
        'days': 24
    }
    result = elapsed_ns
    for unit, divider in dividers.items():
        result /= divider
        if result < 100:
            return f'{result:.1f} {unit}'
        else:
            result = round(result)


def emul_time_ns():
    return int(perf_counter() * 10 ** 9)


class Timer:
    def __init__(self):
        pass

    def __enter__(self):
        self.start = time_ns()
        return self

    def __exit__(self, *args):
        pass

    @property
    def ns(self):
        return time_ns() - self.start

    @property
    def pretty(self):
        return pretty_ns(self.ns)


import time
try:
    time_ns = time.time_ns
except AttributeError:
    from time import perf_counter
    time_ns = emul_time_ns


if __name__ == "__main__":
    import doctest
    doctest.testmod()
