class Command:

    target_floor: int = None

    exchange_flag = None
    exchange_needed: int = None

    call_sender_id = None

    def __init__(self, *, move_to_floor: int, make_exchange: bool = True, exchange_flag=None, call_sender_id=None):
        self.target_floor = move_to_floor
        self.exchange_flag = exchange_flag
        self.exchange_needed = make_exchange
        self.call_sender_id = call_sender_id

    def __str__(self):
        string = "<Command: "
        if self.target_floor is not None:
            string += f"move to floor {self.target_floor}, "
        if self.exchange_needed:
            string += f"make exchange with flag {self.exchange_flag}, "
        if self.call_sender_id is not None:
            string += f"drop controller #{self.call_sender_id} state, "
        return (string[:-2] if string.endswith(', ') else string) + '>'

    def __repr__(self):
        return self.__str__()
