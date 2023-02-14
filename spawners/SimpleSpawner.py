import random as rnd
from typing import Iterable

import pylvtmod as md
from pylvtmod import Ticket, Model


class SimpleSpawner(md.TicketsFactory, md.ModelPostConfigurableObject):

    _floors_count_: int = None

    def setup(self, model: Model):
        self._floors_count_ = model.building.floors.count()

    def generate_tickets(self, time, ticks) -> Iterable[Ticket]:
        if time % 180 == 0:
            return [md.Ticket(departure=1, destination=rnd.randint(2, self._floors_count_))]

        if time % 600 == 0:
            return [md.Ticket(departure=rnd.randint(2, self._floors_count_), destination=1)]

        return []
