from abc import abstractmethod
from typing import Any, Union, Iterable, Dict


class ModelStateInfoSupplier:

    @abstractmethod
    def get_name(self, time, ticks) -> str:
        pass

    @abstractmethod
    def get_info(self, time, ticks) -> Union[str, Iterable[Any], Dict[Any, Any]]:
        pass

    @abstractmethod
    def get_info_str(self, time, ticks) -> str:
        return tabulate(
            [
                [self._model_.time(), "Model time"],
                [self._model_.ticks(), "Ticks from start"]
            ],
            colalign=['right', 'left'],
            tablefmt='plain')
