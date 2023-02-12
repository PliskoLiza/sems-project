from abc import abstractmethod

from .. import Passenger


class PassengersDataCollector:

    @abstractmethod
    def register_passenger(self, passenger: Passenger):
        pass
