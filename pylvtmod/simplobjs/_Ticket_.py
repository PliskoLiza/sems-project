class Ticket:

    departure_floor: int = None
    destination_floor: int = None

    def __init__(self, departure: int, destination: int):
        self.destination_floor = destination
        self.departure_floor = departure

    def __str__(self):
        return f"<Ticket: {self.departure_floor} -> {self.destination_floor}>"

    def __repr__(self):
        return self.__str__()
