import random as rnd
from typing import Iterable

import pylvtmod as md
from pylvtmod import Ticket, Model


class SimpleSpawner(md.TicketsFactory, md.ModelPostConfigurableObject):

    _floors_count_: int = None

    def setup(self, model: Model):
        self._floors_count_ = model.building.floors.count()

    def generate_tickets(self, time) -> Iterable[Ticket]:
        if time % 60 == 0:
            return [md.Ticket(departure=1, destination=rnd.randint(2, self._floors_count_))]

        return []
