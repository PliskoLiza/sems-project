from typing import Dict, Any

from .. import ModelConfiguration, ModelPreConfigurableObject
from .. import LiftCabinSpecificsFactory, LiftCabinPositionsFactory, RequestReceiversFactory
from . import Floor, Floors, LiftCabin


class LiftCabinsFactory(ModelPreConfigurableObject):

    _floors_: Floors = None

    _request_receivers_factory_: RequestReceiversFactory = None

    _cabin_specifics_factory_: LiftCabinSpecificsFactory = None
    _cabin_positions_factory_: LiftCabinPositionsFactory = None

    def __init__(self, *args, floors: Floors, **kwargs):
        super().__init__(*args, **kwargs)
        self._floors_ = floors

    def configure(self, configuration: ModelConfiguration):
        self._request_receivers_factory_ = configuration.request_receivers_factory
        self._cabin_specifics_factory_ = configuration.lift_cabin_specifics_factory
        self._cabin_positions_factory_ = configuration.lift_cabin_positions_factory

    def create_lift_cabins(self) -> Dict[Any, LiftCabin]:
        receivers = self._request_receivers_factory_.get_request_receivers()
        specifics = self._cabin_specifics_factory_.get_cabins_specifics()
        positions = self._cabin_positions_factory_.get_cabins_positions()
        return {key: LiftCabin(key,
                               floors=self._floors_,
                               specific=specifics[key],
                               position=positions[key],
                               receiver=receivers[key])
                for key in specifics.keys()}
