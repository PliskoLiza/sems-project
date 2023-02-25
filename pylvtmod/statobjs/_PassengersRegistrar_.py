from typing import List

from .. import Passenger, PassengersDataCollector


class PassengersRegistrar(PassengersDataCollector):

    passengers: List[Passenger] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passengers = list()

    def register_passenger(self, passenger: Passenger):
        self.passengers.append(passenger)
