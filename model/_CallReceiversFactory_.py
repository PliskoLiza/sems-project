from abc import abstractmethod
from typing import Iterable

from model._CallReceiver_ import CallReceiver
from model._Floor_ import Floor


class CallReceiversFactory:

    @abstractmethod
    def get_receivers_for(self, floor: Floor) -> Iterable[CallReceiver]:
        pass
