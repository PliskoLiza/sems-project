from typing import Dict, Any
from abc import abstractmethod

from llist import dllist

from pylvtmod import *


class LiveLiftController(CallReceiver, RequestReceiver, ModelLiveObject, ModelPostConfigurableObject):

    model: Model = None
    lifts: Dict[Any, LiftCabin] = None
    flagging_provider: FlaggingProvider = None

    calls: dllist = None
    requests: dllist = None

    def __init__(self, *_, **__):
        self.calls = dllist()
        self.requests = dllist()

    def setup(self, model: Model):
        self.model = model
        self.lifts = model.building.lifts
        self.flagging_provider = model.configuration.flagging_provider
        model.tick_actions.append(self)

    def has_requests(self) -> bool:
        return self.requests.first is not None

    def has_calls(self) -> bool:
        return self.calls.first is not None

    def pop_request(self) -> Request:
        return self.requests.popleft()

    def pop_call(self) -> Call:
        return self.calls.popright()

    def push_request(self, request: Request):
        self.requests.append(request)

    def push_call(self, call: Call):
        self.calls.append(call)

    @abstractmethod
    def tick(self, time, ticks):
        pass
