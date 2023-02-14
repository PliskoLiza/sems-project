from abc import abstractmethod
from typing import Any


class TimeCounter:

    @abstractmethod
    def current(self) -> Any:
        pass

    @abstractmethod
    def tick(self) -> Any:
        pass

    @abstractmethod
    def ticks2interval(self, ticks):
        pass

    @abstractmethod
    def interval2ticks(self, interval):
        pass
