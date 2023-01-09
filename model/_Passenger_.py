from typing import List, Tuple, Any, Dict

from ._PassengerStates_ import PassengerStates
from ._Ticket_ import Ticket


class Passenger:

    passenger_id = None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.passenger_id == self.passenger_id

    def __hash__(self):
        return hash(id)

    ticket: Ticket = None
    states: Dict[PassengerStates, Any] = None

    def __init__(self, passenger_id, *, ticket: Ticket):
        self.passenger_id = passenger_id
        self.states = dict()
        self.ticket = ticket

    def try_update_state(self, time, state: PassengerStates):
        if state not in self.states:
            self.states.update({state: time})
