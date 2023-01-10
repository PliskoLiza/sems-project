from linklst import LinkedList
from typing import Dict, Any, Iterable, Union

from .. import ModelConfiguration
from .. import FlaggingProvider
from .. import PassengerStates, Passenger, Waiter, FloorPlan
from . import FloorController, FloorControllersFactory


class Floor:

    number: int = None
    plan: FloorPlan = None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.number == self.number

    def __hash__(self):
        return hash(self.number)

    queue: LinkedList = None
    controllers: Dict[Any, FloorController] = None

    def has_inactive_controllers(self):
        return any(map(self.controllers.values(), lambda controller: not controller.active()))

    def inactive_controllers(self):
        return filter(self.controllers.values(), lambda controller: not controller.active())

    def has_controllers_with_state(self, state: PassengerStates):
        return any(map(self.controllers.values(), lambda controller: controller.state == state))

    def controllers_with_state(self, state: PassengerStates):
        return filter(self.controllers.values(), lambda controller: controller.state == state)

    def waiters_with_flag(self, flag, *, unwrap=True) -> Iterable[Union[Waiter, LinkedList.Element]]:
        return filter(self.queue.iterate(unwrap=unwrap),
                      (lambda waiter: waiter.flag == flag) if unwrap
                      else (lambda waiter: waiter.value.flag == flag))

    flagging_provider: FlaggingProvider = None

    def __init__(self, number: int, *,
                 plan: FloorPlan,
                 controllers: Dict[Any, FloorController],
                 flagging_provider: FlaggingProvider):

        self.number = number
        self.plan = plan
        self.queue = LinkedList()
        self.controllers = controllers
        self.flagging_provider = flagging_provider

    def push_passenger(self, time, passenger: Passenger):
        passenger.try_update_state(time, PassengerStates.WAITING_AT_FLOOR)
        waiter = Waiter(passenger, self.flagging_provider.get_flag_for(passenger.ticket))
        self.queue.appendleft(waiter)
        self.try_register_waiter(waiter)

    def pickup_passengers(self, flag, maximum_count, *, caller_id=None) -> Iterable[Passenger]:
        counter = 0
        for waiter_element in self.waiters_with_flag(flag=flag, unwrap=False):
            counter += 1
            if counter <= maximum_count:
                yield waiter_element.truncate()
            else:
                break
        self.drop_controllers(flag, controller_id=caller_id)

    def drop_controllers(self, flag, *, controller_id=None):
        if controller_id is not None:
            self.controllers[controller_id].drop_state()
        else:
            for controller in self.controllers_with_state(flag):
                controller.drop_state()
        self.drop_waiters_registration(flag)

    def try_register_waiter(self, waiter: Waiter):
        for controller in self.inactive_controllers():
            if controller.try_set_state(waiter.flag):
                waiter.registered = True
                return
        if self.has_controllers_with_state(waiter.flag):
            waiter.registered = True

    def update_waiters_registration(self):
        for waiter in self.queue:
            self.try_register_waiter(waiter)

    def drop_waiters_registration(self, state):
        if not self.has_controllers_with_state(state):
            for waiter in self.waiters_with_flag(state):
                waiter.registered = False
        self.update_waiters_registration()
