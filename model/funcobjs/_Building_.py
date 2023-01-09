from typing import List

from .. import ModelConfiguration
from .. import Passenger
from . import Floor, FloorControllersFactory


class Building:

    floors_count: int = None
    floors: List[Floor] = None

    def __init__(self, *, configuration: ModelConfiguration):
        self.configure(configuration)

    def configure(self, configuration: ModelConfiguration):
        self.floors_count = configuration.floors_count
        controllers_factory = FloorControllersFactory(configuration=configuration)
        self.floors = [Floor(i, configuration=configuration, controllers_factory=controllers_factory)
                       for i in range(1, configuration.floors_count + 1)]

    def push_passenger(self, time, passenger: Passenger):
        self.floors[passenger.ticket.departure_floor].push_passenger(time, passenger)
