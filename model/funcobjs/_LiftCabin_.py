from .. import ModelLiveObject
from .. import LiftCabinSpecific, LiftCabinPosition


class LiftCabin(ModelLiveObject):

    cabin_id = None
    specific: LiftCabinSpecific = None
    position: LiftCabinPosition = None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.cabin_id == self.cabin_id

    def __hash__(self):
        return hash(self.cabin_id)

    def __init__(self, cabin_id, *, specific: LiftCabinSpecific, position: LiftCabinPosition):
        self.cabin_id = cabin_id
        self.specific = specific
        self.position = position

    def tick(self, time):
        pass
