from model._Passenger_ import Passenger


class Waiter:

    flag = None
    passenger: Passenger = None
    registered: bool = None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.passenger == self.passenger

    def __hash__(self):
        return hash(self.passenger)

    def __init__(self, passenger: Passenger, flag):
        self.registered = False
        self.passenger = passenger
        self.flag = flag
