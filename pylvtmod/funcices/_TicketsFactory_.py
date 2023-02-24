from typing import Iterable
from abc import abstractmethod

from .. import Ticket


class TicketsFactory:

    @abstractmethod
    def generate_tickets(self, time, ticks) -> Iterable[Ticket]:
        pass
