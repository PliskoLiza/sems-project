class LiftCabinPosition:

    floor: int = None
    elevation: float = None

    def __init__(self, *, floor=1, elevation=0):
        self.floor = floor
        self.elevation = elevation

    def __str__(self):
        return f"<CabinPosition: floor {self.floor}, elevation {self.elevation}>"

    def __repr__(self):
        return self.__str__()
