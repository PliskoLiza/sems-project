from linklst import LinkedList

from .. import ModelLiveObject
from .. import Passenger, PassengerStates, LiftCabinSpecific, LiftCabinPosition, Request, RequestReceiver
from . import Floors


class LiftCabin(ModelLiveObject):

    cabin_id = None
    specific: LiftCabinSpecific = None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.cabin_id == self.cabin_id

    def __hash__(self):
        return hash(self.cabin_id)

    floors: Floors = None
    position: LiftCabinPosition = None

    commands: LinkedList = None
    receiver: RequestReceiver = None

    amount: int = None
    passengers: LinkedList = None

    def __init__(self, cabin_id, *,
                 specific: LiftCabinSpecific,
                 position: LiftCabinPosition,
                 receiver: RequestReceiver,
                 floors: Floors):

        self.cabin_id = cabin_id
        self.specific = specific

        self.floors = floors
        self.position = position

        self.commands = LinkedList()
        self.receiver = receiver

        self.amount = 0
        self.passengers = LinkedList()

    def make_exchange(self, time, *, flag, caller_id=None):
        for element in self.passengers.iterate(unwrap=False):
            if element.value.ticket.destination_floor == self.position.floor:
                passenger: Passenger = element.truncate()
                self.amount -= 1
                passenger.try_update_state(time, PassengerStates.ARRIVED)

        destinations = set()

        for passenger in self.floors[self.position.floor].pickup_passengers(flag, self.specific.capacity - self.amount,
                                                                            caller_id=caller_id):
            destinations.add(passenger.ticket.destination_floor)
            self.passengers.append(passenger)
            self.amount += 1

        self.receiver.push_request(Request(sender_id=self.cabin_id, destinations=destinations))

    def tick(self, time):
        if not self.commands.isEmpty():
            if self.move(self.commands.first().target_floor):
                command = self.commands.pop()
                if command.exchange_needed:
                    self.make_exchange(time, flag=command.exchange_flag, caller_id=command.call_sender_id)

    def move(self, target_floor) -> bool:
        if target_floor is None:
            return self.position.elevation == 0

        if self.position.floor < target_floor:
            self.position.elevation += self.specific.speed
            if self.position.elevation >= self.floors[self.position.floor].plan.height:
                self.position.elevation -= self.floors[self.position.floor].plan.height
                self.position.floor += 1
                if self.position.floor == target_floor:
                    self.position.elevation = 0
                    return True
                return False

        self.position.elevation -= self.specific.speed
        if self.position.elevation <= 0:
            if self.position.floor == target_floor:
                self.position.elevation = 0
                return True
            self.position.floor -= 1
            self.position.elevation += self.floors[self.position.floor].plan.height
            return False
