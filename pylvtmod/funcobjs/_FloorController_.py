from .. import Call, CallReceiver


class FloorController:

    controller_id = None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.controller_id == self.controller_id

    def __hash__(self):
        return hash(self.controller_id)

    state = None
    floor: int = None
    receiver: CallReceiver = None

    def __init__(self, controller_id, *, floor: int, receiver: CallReceiver):
        self.controller_id = controller_id
        self.receiver = receiver
        self.floor = floor

    def active(self):
        return self.state is not None

    def try_set_state(self, new_state) -> bool:
        if self.active():
            return self.state == new_state
        self.state = new_state
        self.receiver.push_call(Call(sender_id=self.controller_id, floor=self.floor, flag=self.state))
        return True

    def drop_state(self):
        self.state = None
