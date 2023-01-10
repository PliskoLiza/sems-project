from abc import abstractmethod
from typing import Dict, Any

from .. import LiftCabinPosition


class LiftCabinPositionsFactory:

    @abstractmethod
    def get_cabins_positions(self) -> Dict[Any, LiftCabinPosition]:
        pass
