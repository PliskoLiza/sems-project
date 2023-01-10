from abc import abstractmethod
from typing import Iterable

from . import CallReceiver


class CallReceiversFactory:

    @abstractmethod
    def get_call_receivers_for(self, floor: int) -> Iterable[CallReceiver]:
        pass
