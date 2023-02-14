from typing import Iterable, Callable, List, Union

from . import ModelConfiguration, ModelPreConfigurableObject, ModelLiveObject
from . import TimeCounter, TicketsFactory
from . import Building, PassengersFactory


class Model(ModelLiveObject, ModelPreConfigurableObject):

    configuration: ModelConfiguration = None

    building: Building = None

    _ticks_from_start_: int = None

    time_counter: TimeCounter = None
    tick_actions: List[Union[Callable, ModelLiveObject]] = None

    tickets_factory: TicketsFactory = None
    passengers_factory: PassengersFactory = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tick_actions = [self.spawn_passengers, self.building]
        self._ticks_from_start_ = 0

    def configure(self, configuration: ModelConfiguration):
        self.configuration = configuration
        self.building = Building(configuration=configuration)
        self.passengers_factory = PassengersFactory(configuration=configuration)
        self.time_counter = configuration.time_counter
        self.tickets_factory = configuration.tickets_factory

    def run(self, condition):
        while condition(self):
            self.run_tick()

    def time(self):
        return self.time_counter.current()

    def ticks(self):
        return self._ticks_from_start_

    def run_tick(self):
        self.time_counter.tick()
        self._ticks_from_start_ += 1
        self.tick(self.time(), self.ticks())

    def tick(self, time, ticks):
        for action in self.tick_actions:
            if isinstance(action, ModelLiveObject):
                action.tick(time, ticks)
            else:
                action(time, ticks)

    def spawn_passengers(self, time, ticks):
        for ticket in self.tickets_factory.generate_tickets(time, ticks):
            self.building.push_passenger(self.time(), self.passengers_factory.spawn_passenger(ticket))
