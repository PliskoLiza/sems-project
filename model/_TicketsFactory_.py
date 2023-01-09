from typing import Iterable
from abc import abstractmethod

from ._Building_ import Building
from ._Ticket_ import Ticket


class TicketsFactory:

    building: Building = None

    def __init__(self, *, building: Building):
        self.building = building

    @abstractmethod
    def tick_tickets(self, time) -> Iterable[Ticket]:
        pass
