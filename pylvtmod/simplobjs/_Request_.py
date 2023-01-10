from typing import Set


class Request:

    sender_id = None
    destinations: Set[int] = None

    def __init__(self, *, sender_id, destinations: Set[int]):
        self.sender_id = sender_id
        self.destinations = destinations
