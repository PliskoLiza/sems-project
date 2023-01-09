from typing import Iterable

from ._Building_ import Building
from ._ModelConfiguration_ import ModelConfiguration
from ._PassengerFactory_ import PassengersFactory
from ._TicketsFactory_ import TicketsFactory
from ._TimeCounter_ import TimeCounter


class Model:

    building: Building = None

    time_counter: TimeCounter = None

    tickets_factory: TicketsFactory = None
    passengers_factory: PassengersFactory = None

    def __init__(self, *, configuration: ModelConfiguration):
        self.configure(configuration)

    def configure(self, configuration: ModelConfiguration):
        self.building = Building(configuration=configuration)
        self.passengers_factory = PassengersFactory(configuration=configuration)
        self.time_counter = configuration.time_counter
        self.tickets_factory = configuration.tickets_factory

    def time(self):
        return self.time_counter.current()

    def tick(self):
        self.time_counter.tick()
        for ticket in self.tickets_factory.tick_tickets(self.time()):
            self.building.push_passenger(self.time(), self.passengers_factory.spawn_passenger(ticket))

    def run(self, condition) -> Iterable:
        while condition(self):
            self.tick()
