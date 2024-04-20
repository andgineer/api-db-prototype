"""Time elapsed in human lovable form.

- time_ns for Python before 3.7
- Elapsed context manager
- pretty_ns to represent time elapsed in human lovable form

Usage:
>>> start = time_ns()
>>> pass  # code to time
>>> pretty_ns((start + 100) - start)
'0.1 mks'

>>> import time
>>> with Timer() as timer:
...     time.sleep(0.01)
...     timer.pretty.endswith('s')
...     timer.ns > 0
True
True

"""

from typing import Any, Callable, Union
import time

time_ns: Callable[[], int]  # for Python3.7+ this is function from system library time
# for earlier Python versions this is emulation of the Python3.7 time_ns


def pretty_ns(elapsed_ns: Union[int, float]) -> str:
    """Represent time in human lovable form."""
    dividers = {
        "us": 1,
        "mks": 1000,
        "ms": 1000,
        "s": 1000,
        "minutes": 60,
        "hours": 60,
        "days": 24,
    }
    result: float = elapsed_ns
    for unit, divider in dividers.items():
        result /= divider
        if result < 100:
            return f"{result:.1f} {unit}"
        result = round(result)
    raise ValueError(f"Very strange things happen in attempt to represent `{elapsed_ns}`.")


def emul_time_ns() -> int:
    """Emulate time_ns for Python before 3.7."""
    return int(perf_counter() * 10**9)  # pylint: disable=used-before-assignment


class Timer:
    """Context manager to measure time elapsed."""

    def __init__(self) -> None:
        """Initialize Timer."""

    def __enter__(self) -> "Timer":
        """Start measuring time."""
        self.start = time_ns()
        return self

    def __exit__(self, *args: Any) -> None:
        """Stop measuring time."""

    @property
    def ns(self) -> int:
        """Return elapsed time in nanoseconds."""
        return time_ns() - self.start

    @property
    def pretty(self) -> str:
        """Return elapsed time in human lovable form."""
        return pretty_ns(self.ns)


try:
    time_ns = time.time_ns
except AttributeError:
    from time import perf_counter

    time_ns = emul_time_ns


if __name__ == "__main__":
    import doctest

    doctest.testmod()
