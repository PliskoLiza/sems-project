from abc import abstractmethod
from typing import Any


class TimeCounter:

    @abstractmethod
    def current(self) -> Any:
        pass

    @abstractmethod
    def tick(self) -> Any:
        pass
