from typing import Sequence


class Command:

    target_floor: int = None

    exchange_flags: Sequence = None
    exchange_needed: int = None

    call_sender_id = None

    def __init__(self, *,
                 move_to_floor: int,
                 make_exchange: bool = True,
                 load_flag=None,
                 load_flags: Sequence = None,
                 call_sender_id=None):

        self.target_floor = move_to_floor
        self.call_sender_id = call_sender_id
        self.exchange_needed = make_exchange
        self.exchange_flags = ([] if load_flag is None else [load_flag]) if load_flags is None else load_flags

    def __str__(self):
        string = "<Command: "
        if self.target_floor is not None:
            string += f"move to floor {self.target_floor}, "
        if self.exchange_needed:
            string += f"make exchange with flags {self.exchange_flags}, "
        if self.call_sender_id is not None:
            string += f"drop controller #{self.call_sender_id} state, "
        return (string[:-2] if string.endswith(', ') else string) + '>'

    def __repr__(self):
        return self.__str__()
