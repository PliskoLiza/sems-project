from .. import ModelConfiguration, ModelPreConfigurableObject
from .. import FloorPlansFactory, FlaggingProvider
from . import Floor, Floors, FloorControllersFactory


class FloorsFactory(ModelPreConfigurableObject):

    _flagging_provider_: FlaggingProvider
    _controllers_factory_: FloorControllersFactory
    _floor_plans_factory_: FloorPlansFactory

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def configure(self, configuration: ModelConfiguration):
        self._flagging_provider_ = configuration.flagging_provider
        self._floor_plans_factory_ = configuration.floor_plans_factory
        self._controllers_factory_ = FloorControllersFactory(configuration=configuration)

    def get_floors(self) -> Floors:
        plans = self._floor_plans_factory_.get_floor_plans()
        start_number = self._floor_plans_factory_.get_first_floor_number()
        return Floors([Floor(i + start_number,
                             plan=plans[i],
                             flagging_provider=self._flagging_provider_,
                             controllers=self._controllers_factory_.get_controllers_for(i + start_number))
                       for i in range(0, self._floor_plans_factory_.get_floors_count())],
                      start_number=start_number)
