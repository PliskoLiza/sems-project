from typing import List, Iterable

from . import Floor


class Floors:

    start_number: int = None
    _floors_: List[Floor]

    def __init__(self, floors: List[Floor], *, start_number=1):
        self.start_number = start_number
        self._floors_ = floors

    def __iter__(self) -> Iterable[Floor]:
        return iter(self._floors_)

    def reversed(self) -> Iterable[Floor]:
        return reversed(self._floors_)

    def __getitem__(self, item):
        if type(item) is int:
            index = item - self.start_number
            if 0 <= index <= len(self._floors_):
                return self._floors_[index]
        raise IndexError()

    def __len__(self):
        return len(self._floors_)

    def count(self):
        return len(self._floors_)
