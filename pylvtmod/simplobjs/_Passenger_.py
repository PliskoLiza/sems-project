from typing import Any, Union, Dict, Tuple

from . import PassengerStates, Ticket


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

    def passed_states(self, *states: PassengerStates):
        return all(map(lambda state: state in self.states.keys(), states))

    def try_update_state(self, time, state: PassengerStates):
        if state not in self.states:
            self.states.update({state: time})

    def get_time_between(self, state1: PassengerStates, state2: PassengerStates) -> Any:
        try:
            return abs(self.states[state1] - self.states[state2])
        except KeyError:
            return None

    @property
    def state(self) -> Union[None, Tuple[PassengerStates, Any]]:
        try:
            state = max(self.states, key=self.states.__getitem__)
            return state, self.states[state]
        except ValueError:
            return None

    def __str__(self):
        state = self.state
        return f"<Passenger #{self.passenger_id}: {self.ticket}, {state[0]} since {state[1]}>"

    def __repr__(self):
        return self.__str__()
