from abc import abstractmethod
from typing import Iterable

from .. import FloorPlan


class FloorPlansFactory:

    @abstractmethod
    def get_floors_count(self) -> int:
        pass

    @abstractmethod
    def get_floor_plans(self) -> Iterable[FloorPlan]:
        pass
