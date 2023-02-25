from typing import Any, Tuple

from . import PassengersRegistrar
from .. import PassengerStates


class PassengersStatsCollector(PassengersRegistrar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_pass_count(self):
        return len(self.passengers)

    def get_avg_service_time(self):
        return self.get_avf_time_between(PassengerStates.WAITING_AT_FLOOR, PassengerStates.ARRIVED)

    def get_avg_wait_time(self) -> Tuple[Any, int]:
        return self.get_avf_time_between(PassengerStates.WAITING_AT_FLOOR, PassengerStates.MOVING_IN_CABIN)

    def get_avg_trip_time(self) -> Tuple[Any, int]:
        return self.get_avf_time_between(PassengerStates.MOVING_IN_CABIN, PassengerStates.ARRIVED)

    def get_avf_time_between(self, state1: PassengerStates, state2: PassengerStates) -> Tuple[Any, int]:

        summa = 0
        count = 0

        for passenger in self.passengers:
            delta = passenger.get_time_between(state1, state2)
            if delta is not None:
                summa += delta
                count += 1

        return (None, 0) if count == 0 else (summa/count, count)

    def get_servicing_pass_count(self):
        return self.get_pass_count() - self.get_served_pass_count()

    def get_served_pass_count(self):
        return self.get_passed_pass_count(PassengerStates.ARRIVED)

    def get_passed_pass_count(self, *states: PassengerStates):
        return sum(map(lambda passenger: 1 if passenger.passed_states(*states) else 0, self.passengers))

    @staticmethod
    def get_percentage(value, amount, *, rnd: int = None, trunc: bool = False) -> Any:

        if amount == 0:
            return None

        percentage = value / amount * 100

        if trunc:
            return int(percentage)
        if rnd is None:
            return percentage
        return round(percentage, rnd)
