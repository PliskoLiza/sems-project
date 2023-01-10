from typing import List
from abc import abstractmethod

from .. import FloorPlan


class FloorPlansFactory:

    @abstractmethod
    def get_floors_count(self) -> int:
        pass

    @abstractmethod
    def get_first_floor_number(self) -> int:
        pass

    @abstractmethod
    def get_floor_plans(self) -> List[FloorPlan]:
        pass
