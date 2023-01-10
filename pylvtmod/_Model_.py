from typing import Iterable, Callable, List, Union

from . import ModelConfiguration, ModelPreConfigurableObject, ModelLiveObject
from . import TimeCounter, TicketsFactory
from . import Building, PassengersFactory


class Model(ModelLiveObject, ModelPreConfigurableObject):

    building: Building = None

    time_counter: TimeCounter = None
    tick_actions: List[Union[Callable, ModelLiveObject]] = None

    tickets_factory: TicketsFactory = None
    passengers_factory: PassengersFactory = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tick_actions = [self.spawn_passengers, self.building]

    def configure(self, configuration: ModelConfiguration):
        self.building = Building(configuration=configuration)
        self.passengers_factory = PassengersFactory(configuration=configuration)
        self.time_counter = configuration.time_counter
        self.tickets_factory = configuration.tickets_factory

    def run(self, condition) -> Iterable:
        while condition(self):
            self.run_tick()

    def time(self):
        return self.time_counter.current()

    def run_tick(self):
        self.time_counter.tick()
        self.tick(self.time())

    def tick(self, time):
        for action in self.tick_actions:
            if isinstance(action, ModelLiveObject):
                action.tick(time)
            else:
                action(time)

    def spawn_passengers(self, time):
        for ticket in self.tickets_factory.generate_tickets(time):
            self.building.push_passenger(self.time(), self.passengers_factory.spawn_passenger(ticket))
