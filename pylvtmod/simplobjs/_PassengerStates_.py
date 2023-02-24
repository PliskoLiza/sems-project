from enum import Enum


class PassengerStates(Enum):
    WAITING_AT_FLOOR = 1
    MOVING_IN_CABIN = 2
    ARRIVED = 3
