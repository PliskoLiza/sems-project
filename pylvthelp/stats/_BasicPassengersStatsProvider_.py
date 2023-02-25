from typing import Union, Iterable, Any, Dict

from pylvtmod import PassengersStatsCollector
from .. import ModelStateDictInfoSupplier


class BasicPassengersStatsProvider(ModelStateDictInfoSupplier, PassengersStatsCollector):

    _supplier_name_: str = None

    def __init__(self, *args, supplier_name='statistics', **kwargs):
        super().__init__(*args, **kwargs)
        self._supplier_name_ = supplier_name

    def get_name(self, time, ticks) -> str:
        return self._supplier_name_

    def get_info(self, time, ticks) -> Union[str, Iterable[Any], Dict[Any, Any]]:
        return {
            "Total passengers generated": self.get_pass_count(),
            "Total passengers served": self.get_served_pass_count(),
            "Served passengers percentage": self.get_percentage(self.get_served_pass_count(), self.get_pass_count(),
                                                                rnd=4),
            "Average waiting time": self.get_avg_wait_time()[0],
            "Average elevation time": self.get_avg_trip_time()[0],
            "Average servicing time": self.get_avg_service_time()[0]
        }
