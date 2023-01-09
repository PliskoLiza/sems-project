from typing import Any

from model._TimeCounter_ import TimeCounter


class SimpleTimeCounter(TimeCounter):

    _time_: int = None

    def __init__(self):
        self._time_ = 0

    def current(self) -> Any:
        return self._time_

    def tick(self) -> Any:
        self._time_ += 1
        return self._time_
