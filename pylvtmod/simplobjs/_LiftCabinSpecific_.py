class LiftCabinSpecific:

    speed: float = None
    capacity: int = None

    unload_ticks: int = None
    load_ticks: int = None

    def __init__(self, *, speed: float, capacity: int, unload_ticks: int, load_ticks: int):

        self.capacity = capacity
        self.speed = speed

        self.load_ticks = load_ticks
        self.unload_ticks = unload_ticks
