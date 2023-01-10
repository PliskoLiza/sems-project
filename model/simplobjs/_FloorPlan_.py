class FloorPlan:

    height: float = None

    def __init__(self, number: int, *, height: float = None):
        self.number = number
        self.height = height
