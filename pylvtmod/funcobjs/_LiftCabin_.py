from typing import Sequence

from llist import dllist

from .. import ModelLiveObject
from .. import PassengerStates
from .. import Command, Request, RequestReceiver
from .. import LiftCabinSpecific, LiftCabinPosition, LiftCabinState
from . import LiftCabinStateManager, LiftCabinCommandsManager
from . import Floors


class LiftCabin(ModelLiveObject):

    cabin_id = None
    specific: LiftCabinSpecific = None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.cabin_id == self.cabin_id

    def __hash__(self):
        return hash(self.cabin_id)

    state: LiftCabinStateManager = None

    floors: Floors = None
    position: LiftCabinPosition = None

    commands: LiftCabinCommandsManager = None
    receiver: RequestReceiver = None

    passnumber: int = None
    passengers: dllist = None

    def __init__(self, cabin_id, *,
                 specific: LiftCabinSpecific,
                 position: LiftCabinPosition,
                 receiver: RequestReceiver,
                 floors: Floors):

        self.cabin_id = cabin_id
        self.specific = specific

        self.state = LiftCabinStateManager()

        self.floors = floors
        self.position = position

        self.commands = LiftCabinCommandsManager()
        self.receiver = receiver

        self.passnumber = 0
        self.passengers = dllist()

    def tick(self, time, ticks):
        self.state.tick(time, ticks)
        if self.state.available() and not self.commands.empty():
            if self.execute(time, self.commands.active):
                self.commands.pop()

    def execute(self, time, command: Command):
        if self.move(command.target_floor):
            if command.exchange_needed:
                self.make_exchange(time, flags=command.exchange_flags, caller_id=command.call_sender_id)
            self.state.try_drop()
            return True
        return False

    def move(self, target_floor) -> bool:
        if target_floor is None:
            return self.position.elevation == 0
        return self.move_up(target_floor) if self.position.floor < target_floor else self.move_down(target_floor)

    def move_up(self, target_floor):
        self.state.value = LiftCabinState.MovingUP
        self.position.elevation += self.specific.speed
        if self.position.elevation >= self.floors[self.position.floor].plan.height:
            self.position.elevation -= self.floors[self.position.floor].plan.height
            self.position.floor += 1
            if self.position.floor == target_floor:
                self.position.elevation = 0
                return True
            return False

    def move_down(self, target_floor):
        self.state.value = LiftCabinState.MovingDOWN
        self.position.elevation -= self.specific.speed
        if self.position.elevation <= 0:
            if self.position.floor == target_floor:
                self.position.elevation = 0
                return True
            self.position.floor -= 1
            self.position.elevation += self.floors[self.position.floor].plan.height
            return False

    def make_exchange(self, time, *, flags: Sequence, caller_id=None):
        self.unload(time)
        destinations = self.load(time, flags=flags, caller_id=caller_id)
        self.receiver.push_request(Request(sender_id=self.cabin_id, destinations=destinations))

    def load(self, time, *, flags: Sequence, caller_id):
        maximum_count = self.specific.capacity - self.passnumber
        passengers = self.floors[self.position.floor].pickup_passengers(flags, maximum_count, caller_id=caller_id)
        destinations = set()
        for passenger in passengers:
            destinations.add(passenger.ticket.destination_floor)
            passenger.try_update_state(time, PassengerStates.MOVING_IN_CABIN)
            self.state.block(LiftCabinState.UnderEXCHANGE, self.specific.load_ticks)
            self.passengers.append(passenger)
            self.passnumber += 1
        return destinations

    def unload(self, time):
        current = self.passengers.first
        while current is not None:
            nxt = current.next
            if current.value.ticket.destination_floor == self.position.floor:
                passenger = self.passengers.remove(current)
                passenger.try_update_state(time, PassengerStates.ARRIVED)
                self.state.block(LiftCabinState.UnderEXCHANGE, self.specific.unload_ticks)
                self.passnumber -= 1
            current = nxt
