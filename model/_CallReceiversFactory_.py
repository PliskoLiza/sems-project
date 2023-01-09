from abc import abstractmethod
from typing import Iterable

from model._CallReceiver_ import CallReceiver


class CallReceiversFactory:

    @abstractmethod
    def get_receivers_for(self, floor: int) -> Iterable[CallReceiver]:
        pass
