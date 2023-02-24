from typing import Iterable, Any

from pylvtmod import *


class UpDownFlaggingProvider(FlaggingProvider):

    def get_flag_sign(self, flag: Any):
        if flag == 'up':
            return '↑'

        if flag == 'dn':
            return '↓'

        if flag is None:
            return '-'

        raise ValueError(f"Unknown flag '{flag}'")

    def get_all_flags(self) -> Iterable[Any]:
        return ['up', 'dn']

    def get_flag_for(self, ticket: Ticket) -> Any:
        return 'up' if ticket.destination_floor > ticket.departure_floor else 'dn'
