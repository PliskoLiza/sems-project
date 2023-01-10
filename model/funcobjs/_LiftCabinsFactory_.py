from typing import Dict, Any

from .. import ModelConfiguration, ModelConfigurableObject
from .. import LiftCabinSpecificsFactory, LiftCabinPositionsFactory
from . import LiftCabin, LiftCabinsFeed


class LiftCabinsFactory(ModelConfigurableObject):

    _cabins_feed_: LiftCabinsFeed
    _cabin_specifics_factory_: LiftCabinSpecificsFactory
    _cabin_positions_factory_: LiftCabinPositionsFactory

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def configure(self, configuration: ModelConfiguration):
        self._cabin_specifics_factory_ = configuration.lift_cabin_specifics_factory
        self._cabin_positions_factory_ = configuration.lift_cabin_positions_factory

    def create_lift_cabins(self) -> Dict[Any, LiftCabin]:
        specifics = self._cabin_specifics_factory_.get_cabins_specifics()
        positions = self._cabin_positions_factory_.get_cabins_positions()
        cabins = {key: LiftCabin(key, specific=specifics[key], position=positions[key]) for key in specifics}
        self._cabins_feed_.supply_cabins(cabins)
        return cabins
