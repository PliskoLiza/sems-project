from typing import Any, Dict
from abc import abstractmethod

from .. import LiftCabinSpecific


class LiftCabinSpecificsFactory:

    @abstractmethod
    def get_cabins_specifics(self) -> Dict[Any, LiftCabinSpecific]:
        pass
