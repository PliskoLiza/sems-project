class LiftCabinSpecific:

    speed: float = None
    capacity: int = None

    def __init__(self, *, speed: float, capacity: int):
        self.capacity = capacity
        self.speed = speed
