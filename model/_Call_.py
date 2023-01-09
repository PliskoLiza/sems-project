class Call:

    sender_id = None
    floor: int = None
    flag = None

    def __init__(self, *, sender_id, floor: int, flag):
        self.sender_id = sender_id
        self.floor = floor
        self.flag = flag
