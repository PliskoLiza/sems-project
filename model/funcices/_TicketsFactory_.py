from typing import Iterable
from abc import abstractmethod

from .. import Ticket


class TicketsFactory:

    @abstractmethod
    def tick_tickets(self, time) -> Iterable[Ticket]:
        pass
