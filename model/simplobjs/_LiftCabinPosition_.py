class LiftCabinPosition:

    floor: int = None
    elevation: float = None

    def __init__(self, *, floor=1, elevation=0):
        self.floor = floor
        self.elevation = elevation
