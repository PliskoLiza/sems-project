from typing import Dict, Any, Iterable, Sequence

from . import FloorController


class FloorControllers:

    _controllers_: Dict[Any, FloorController] = None

    def all_active(self) -> bool:
        return all(map(lambda controller: not controller.active(), self._controllers_.values()))

    def inactive(self) -> Iterable[FloorController]:
        return filter(lambda controller: not controller.active(), self._controllers_.values())

    def state_exists(self, state) -> bool:
        return any(map(lambda controller: controller.state == state, self._controllers_.values()))

    def any_state_exists(self, states) -> bool:
        return any(map(lambda controller: controller.state in states, self._controllers_.values()))

    def with_state(self, state) -> Iterable[FloorController]:
        return filter(lambda controller: controller.state == state, self._controllers_.values())

    def with_states(self, state) -> Iterable[FloorController]:
        return filter(lambda controller: controller.state in state, self._controllers_.values())

    def __init__(self, controllers: Dict[Any, FloorController]):
        self._controllers_ = controllers

    def __iter__(self):
        return iter(self._controllers_.values())

    def __len__(self):
        return len(self._controllers_)

    def count(self):
        return len(self._controllers_)

    def __getitem__(self, item):
        return self._controllers_[item]

    def get(self, controller_id):
        return self._controllers_[controller_id]

    def drop(self, *, state=None, states: Sequence = None, controller_id=None):
        if controller_id is not None:
            self._controllers_[controller_id].drop_state()
        else:
            for controller in (self.with_states(states) if state is not None else self.with_state(state)):
                controller.drop_state()

    def state_of(self, controller_id):
        return self._controllers_[controller_id].state

    def try_activate(self, state, *, controller_id=None, reuse=True, reuse_always=False):
        if controller_id is not None:
            controller = self._controllers_[controller_id]
            if not controller.active():
                return controller.try_set_state(state)
            else:
                return controller.state == state and (reuse or reuse_always)

        if reuse_always and self.state_exists(state):
            return True

        for controller in self.inactive():
            if controller.try_set_state(state):
                return True

        if reuse and self.state_exists(state):
            return True

        return False
