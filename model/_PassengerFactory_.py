from ._ModelConfiguration_ import ModelConfiguration
from ._IdFactory_ import IdFactory
from ._Passenger_ import Passenger
from ._Ticket_ import Ticket


class PassengersFactory:

    _id_factory_: IdFactory = None

    def __init__(self, *, configuration: ModelConfiguration):
        self.configure(configuration)

    def configure(self, configuration: ModelConfiguration):
        self._id_factory_ = configuration.passengers_id_factory

    def spawn_passenger(self, ticket: Ticket) -> Passenger:
        return Passenger(self._id_factory_.new_id(), ticket=ticket)
