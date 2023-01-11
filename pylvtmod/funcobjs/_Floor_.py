from llist import dllist
from typing import Iterable

from .. import FlaggingProvider
from .. import PassengerStates, Passenger, Waiter, FloorPlan
from . import FloorControllers


class Floor:

    number: int = None
    plan: FloorPlan = None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.number == self.number

    def __hash__(self):
        return hash(self.number)

    queue: dllist = None
    controllers: FloorControllers = None
    flagging_provider: FlaggingProvider = None

    def __init__(self, number: int, *,
                 plan: FloorPlan,
                 controllers: FloorControllers,
                 flagging_provider: FlaggingProvider):

        self.number = number
        self.plan = plan
        self.queue = dllist()
        self.controllers = controllers
        self.flagging_provider = flagging_provider

    def push_passenger(self, time, passenger: Passenger):
        passenger.try_update_state(time, PassengerStates.WAITING_AT_FLOOR)
        waiter = Waiter(passenger, self.flagging_provider.get_flag_for(passenger.ticket))
        self.queue.append(waiter)
        self.try_register_waiter(waiter)

    def pickup_passengers(self, flags, maximum_count, *, caller_id=None) -> Iterable[Passenger]:
        if len(flags) > 0:
            current = self.queue.first
            counter = 0
            while counter < maximum_count and current is not None:
                nxt = current.next
                if current.value.has_flag_in(flags):
                    yield self.queue.remove(current)
                    counter += 1
                current = nxt
            self.controllers.drop(states=flags, controller_id=caller_id)
            self.drop_waiters_registration(flags)

    def try_register_waiter(self, waiter: Waiter) -> bool:
        registration = self.controllers.try_activate(state=waiter.flag)
        waiter.registered = registration
        return registration

    def update_waiters_registration(self):
        for waiter in self.queue:
            self.try_register_waiter(waiter)

    def drop_waiters_registration(self, flags):
        for flag in flags:
            if not self.controllers.state_exists(flag):
                for waiter in filter(lambda wtr: wtr.has_flag(flag), self.queue):
                    waiter.registered = False
        self.update_waiters_registration()
