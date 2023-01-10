from typing import Dict, Any

from .. import ModelConfiguration, ModelPreConfigurableObject, ModelLiveObject
from .. import Passenger
from . import Floors, LiftCabin, FloorsFactory, LiftCabinsFactory


class Building(ModelPreConfigurableObject, ModelLiveObject):

    floors: Floors = None
    lifts: Dict[Any, LiftCabin] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def configure(self, configuration: ModelConfiguration):
        self.floors = FloorsFactory(configuration=configuration).get_floors()
        self.lifts = LiftCabinsFactory(configuration=configuration, floors=self.floors).create_lift_cabins()

    def push_passenger(self, time, passenger: Passenger):
        self.floors[passenger.ticket.departure_floor].push_passenger(time, passenger)

    def tick(self, time):
        for lift in self.lifts.values():
            lift.tick(time)
