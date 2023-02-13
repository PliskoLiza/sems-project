from abc import abstractmethod
from typing import Any, Iterable

from .. import Ticket


class FlaggingProvider:

    @abstractmethod
    def get_flag_sign(self, flag: Any):
        pass

    @abstractmethod
    def get_all_flags(self) -> Iterable[Any]:
        pass

    @abstractmethod
    def get_flag_for(self, ticket: Ticket) -> Any:
        pass
