from typing import Iterable

import pylvtmod as md
from pylvtmod import Ticket


class SimpleSpawner(md.TicketsFactory):
    def generate_tickets(self, time) -> Iterable[Ticket]:
        pass
