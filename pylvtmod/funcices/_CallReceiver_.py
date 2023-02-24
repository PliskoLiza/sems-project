from abc import abstractmethod

from .. import Call


class CallReceiver:

    @abstractmethod
    def push_call(self, call: Call):
        pass
