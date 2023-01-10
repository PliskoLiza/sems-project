from typing import List, Dict, Any

from .. import ModelConfiguration, ModelConfigurableObject, ModelLiveObject
from .. import Passenger
from . import Floor, LiftCabin, FloorsFactory, LiftCabinsFactory


class Building(ModelConfigurableObject, ModelLiveObject):

    floors: List[Floor] = None
    lifts: Dict[Any, LiftCabin] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def configure(self, configuration: ModelConfiguration):
        self.floors = FloorsFactory(configuration=configuration).get_floors()
        self.lifts = LiftCabinsFactory(configuration=configuration).create_lift_cabins()

    def floor(self, number: int):
        return self.floors[number - 1]

    def floors_count(self):
        return len(self.floors)

    def push_passenger(self, time, passenger: Passenger):
        self.floor(passenger.ticket.departure_floor).push_passenger(time, passenger)

    def tick(self, time):
        pass
