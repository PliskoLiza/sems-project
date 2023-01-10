from typing import Dict

from .. import ModelConfiguration, ModelConfigurableObject
from .. import FloorPlansFactory, FlaggingProvider
from . import Floor, FloorControllersFactory


class FloorsFactory(ModelConfigurableObject):

    _flagging_provider_: FlaggingProvider
    _controllers_factory_: FloorControllersFactory
    _floor_plans_factory_: FloorPlansFactory

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def configure(self, configuration: ModelConfiguration):
        self._flagging_provider_ = configuration.flagging_provider
        self._floor_plans_factory_ = configuration.floor_plans_factory
        self._controllers_factory_ = FloorControllersFactory(configuration=configuration)

    def get_floors(self) -> Dict[int, Floor]:
        floors = list()
        number = 0
        for plan in self._floor_plans_factory_.get_floor_plans():
            number += 1
            floors.append(Floor(number, plan=plan, flagging_provider=self._flagging_provider_,
                                controllers=self._controllers_factory_.get_controllers_for(number)))
        return floors

