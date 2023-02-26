from llist import dllist

from .. import Command


class LiftCabinCommandsManager:

    queue: dllist = None

    def __init__(self):
        self.queue = dllist()

    def pop(self) -> Command:
        return self.queue.popleft()

    @property
    def active(self) -> Command:
        node = self.queue.first
        return node.value if node is not None else None

    def empty(self) -> bool:
        return self.queue.first is None

    def push(self, command: Command):
        self.queue.appendright(command)
