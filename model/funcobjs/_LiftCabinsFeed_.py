from typing import Dict, Any
from abc import abstractmethod

from . import LiftCabin


class LiftCabinsFeed:

    @abstractmethod
    def supply_cabins(self, cabins: Dict[Any, LiftCabin]):
        pass
