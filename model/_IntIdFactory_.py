from model._IdFactory_ import IdFactory


class IntIdFactory(IdFactory):

    _last_used_id_: int = None

    def __init__(self, *args, initial_id: int = 1, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_used_id_ = initial_id - 1

    def new_id(self) -> int:
        self._last_used_id_ += 1
        return self._last_used_id_
