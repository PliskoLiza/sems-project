from .. import ModelConfiguration
from .. import IdFactory
from .. import Ticket, Passenger
from .. import PassengersDataCollector


class PassengersFactory:

    _id_factory_: IdFactory = None
    _data_collector_: PassengersDataCollector = None

    def __init__(self, *, configuration: ModelConfiguration):
        self.configure(configuration)

    def configure(self, configuration: ModelConfiguration):
        self._id_factory_ = configuration.passengers_id_factory
        self._data_collector_ = configuration.passengers_data_collector

    def spawn_passenger(self, ticket: Ticket) -> Passenger:

        passenger = Passenger(self._id_factory_.new_id(), ticket=ticket)

        if self._data_collector_ is not None:
            self._data_collector_.register_passenger(passenger)

        return passenger
