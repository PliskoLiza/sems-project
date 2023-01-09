from abc import abstractmethod
from typing import Any, Iterable

from ._Ticket_ import Ticket


class FlaggingProvider:

    @abstractmethod
    def get_all_flags(self) -> Iterable[Any]:
        pass

    @abstractmethod
    def get_flag_for(self, ticket: Ticket) -> Any:
        pass
