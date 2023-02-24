class FloorPlan:

    height: float = None

    def __init__(self, *, height: float = None):
        self.height = height

    def __str__(self):
        return f"<FloorPlan: {{height={self.height}}}>"
