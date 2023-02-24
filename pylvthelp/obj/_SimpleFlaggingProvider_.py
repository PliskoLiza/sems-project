from typing import Iterable, Any

from pylvtmod import *


class SimpleFlaggingProvider(FlaggingProvider):

    def get_flag_sign(self, flag: Any):
        if flag == 'pressed':
            return '▣'

        if flag is None:
            return '□'

        raise ValueError(f"Unknown flag '{flag}'")

    def get_all_flags(self) -> Iterable[Any]:
        return ['pressed']

    def get_flag_for(self, ticket: Ticket) -> Any:
        return 'pressed'
