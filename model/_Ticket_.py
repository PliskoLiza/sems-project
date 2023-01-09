class Ticket:

    departure_floor: int = None
    destination_floor: int = None

    def __init__(self, departure: int, destination: int):
        self.destination_floor = destination
        self.departure_floor = departure
