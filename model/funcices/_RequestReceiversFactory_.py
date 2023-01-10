from typing import Any, Dict
from abc import abstractmethod

from . import RequestReceiver


class RequestReceiversFactory:

    @abstractmethod
    def get_receivers(self) -> Dict[Any, RequestReceiver]:
        pass
