from typing import Iterable

from . import ModelConfiguration, ModelConfigurableObject, ModelLiveObject
from . import TimeCounter, TicketsFactory
from . import Building, PassengersFactory


class Model(ModelLiveObject, ModelConfigurableObject):

    building: Building = None

    time_counter: TimeCounter = None

    tickets_factory: TicketsFactory = None
    passengers_factory: PassengersFactory = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def configure(self, configuration: ModelConfiguration):
        self.building = Building(configuration=configuration)
        self.passengers_factory = PassengersFactory(configuration=configuration)
        self.time_counter = configuration.time_counter
        self.tickets_factory = configuration.tickets_factory

    def time(self):
        return self.time_counter.current()

    def tick(self, time):
        for ticket in self.tickets_factory.generate_tickets(self.time()):
            self.building.push_passenger(self.time(), self.passengers_factory.spawn_passenger(ticket))
        self.building.tick(time)

    def run_tick(self):
        self.time_counter.tick()
        self.tick(self.time())

    def run(self, condition) -> Iterable:
        while condition(self):
            self.run_tick()
