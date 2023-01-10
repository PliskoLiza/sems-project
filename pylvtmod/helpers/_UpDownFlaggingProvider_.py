from typing import Iterable, Any

from .. import *


class UpDownFlaggingProvider(FlaggingProvider):

    def get_all_flags(self) -> Iterable[Any]:
        return ['up', 'dn']

    def get_flag_for(self, ticket: Ticket) -> Any:
        return 'up' if ticket.destination_floor > ticket.departure_floor else 'dn'
