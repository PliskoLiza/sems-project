from abc import abstractmethod

from .. import Request


class RequestReceiver:

    @abstractmethod
    def push_request(self, request: Request):
        pass
