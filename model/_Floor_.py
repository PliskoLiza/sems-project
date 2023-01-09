from collections import deque
from typing import Dict, Any, Iterable

from ._FlaggingProvider_ import FlaggingProvider
from ._FloorController_ import FloorController
from ._FloorControllersFactory_ import FloorControllersFactory
from ._ModelConfiguration_ import ModelConfiguration
from ._PassengerStates_ import PassengerStates
from ._Passenger_ import Passenger
from ._Waiter_ import Waiter


class Floor:

    number: int = None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.number == self.number

    def __hash__(self):
        return hash(self.number)

    queue: deque = None
    controllers: Dict[Any, FloorController] = None

    def has_inactive_controllers(self):
        return any(map(self.controllers.values(), lambda ctrl: not ctrl.active()))

    def inactive_controllers(self):
        return filter(self.controllers.values(), lambda ctrl: not ctrl.active())

    def has_controllers_with_state(self, state: PassengerStates):
        return any(map(self.controllers.values(), lambda ctrl: ctrl.state == state))

    def controllers_with_state(self, state: PassengerStates):
        return filter(self.controllers.values(), lambda ctrl: ctrl.state == state)

    def waiters_with_flag(self, flag):
        return filter(self.queue, lambda waiter: waiter.flag == flag)

    flagging_provider: FlaggingProvider = None

    def __init__(self, number, *, controllers_factory: FloorControllersFactory, configuration: ModelConfiguration):
        self.queue = deque()
        self.number = number
        self.configure(configuration)
        self.controllers = controllers_factory.get_controllers_for(self.number)

    def configure(self, configuration: ModelConfiguration):
        self.flagging_provider = configuration.flagging_provider

    def push_passenger(self, time, passenger: Passenger):
        passenger.try_update_state(time, PassengerStates.WAITING_AT_FLOOR)
        waiter = Waiter(passenger, self.flagging_provider.get_flag_for(passenger.ticket))
        self.queue.appendleft(waiter)
        self.try_register_waiter(waiter)

    def pickup_passengers(self, flag, maximum_count, *, caller_id=None) -> Iterable[Passenger]:
        counter = 0
        # Add logic for deleting waiters and returning passengers
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
