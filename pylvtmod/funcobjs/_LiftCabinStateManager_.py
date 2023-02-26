from .. import ModelLiveObject
from .. import LiftCabinState


class LiftCabinStateManager(ModelLiveObject):

    _INITIAL_STATE: LiftCabinState = LiftCabinState.Parked

    _state_: LiftCabinState = None
    _block_ticks_: int = None

    def __init__(self):
        self._state_ = self._INITIAL_STATE
        self._block_ticks_ = 0

    @property
    def value(self) -> LiftCabinState:
        return self._state_

    @value.setter
    def value(self, value: LiftCabinState):
        if self.blocked() or (value not in LiftCabinState.AVAILABLE):
            raise RuntimeError("Unable to set cabin state")
        self._state_ = value

    def try_set(self, state: LiftCabinState) -> bool:
        try:
            self.value = state
            return True
        except RuntimeError:
            return False

    def drop(self):
        if self.available():
            self._state_ = self._INITIAL_STATE
        else:
            raise RuntimeError("Unable to drop state")

    def block(self, state, ticks):
        if self.available() or self._state_ == state:
            self._state_ = state
            self._block_ticks_ += ticks
        else:
            raise RuntimeError("Unable to block cabin state")

    def try_drop(self) -> bool:
        try:
            self.drop()
            return True
        except RuntimeError:
            return False

    def try_block(self, state, ticks) -> bool:
        try:
            self.block(state, ticks)
            return True
        except RuntimeError:
            return False

    def blocked(self) -> bool:
        return self._state_ in LiftCabinState.BLOCKED

    def available(self) -> bool:
        return self._state_ in LiftCabinState.AVAILABLE

    def tick(self, time, ticks):
        if self._block_ticks_ > 0:
            self._block_ticks_ -= 1
            if self._block_ticks_ == 0:
                self._state_ = self._INITIAL_STATE

    def __str__(self):
        return str(self._state_).split('.')[-1]

    def __repr__(self):
        return self.__str__()

    def sign(self):
        return LiftCabinState.get_state_sign(self._state_)
