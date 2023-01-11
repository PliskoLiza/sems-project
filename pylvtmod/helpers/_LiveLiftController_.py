from typing import Dict, Any
from abc import abstractmethod

from llist import dllist

from .. import *


class LiveLiftController(CallReceiver, RequestReceiver, ModelLiveObject, ModelPostConfigurableObject):
    lifts: Dict[Any, LiftCabin] = None

    calls: dllist = None
    requests: dllist = None

    def __init__(self, *_, **__):
        self.calls = dllist()
        self.requests = dllist()

    def setup(self, model: Model):
        self.lifts = model.building.lifts
        model.tick_actions.append(self)

    def push_call(self, call: Call):
        self.calls.append(call)

    def push_request(self, request: Request):
        self.requests.append(request)

    @abstractmethod
    def tick(self, time):
        pass
