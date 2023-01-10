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
