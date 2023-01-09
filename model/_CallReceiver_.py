from abc import abstractmethod

from ._Call_ import Call


class CallReceiver:

    @abstractmethod
    def push_call(self, call: Call):
        pass
