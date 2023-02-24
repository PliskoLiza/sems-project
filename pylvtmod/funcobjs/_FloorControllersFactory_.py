from .. import ModelConfiguration, ModelPreConfigurableObject
from .. import IdFactory
from . import FloorController, FloorControllers


class FloorControllersFactory(ModelPreConfigurableObject):

    _receivers_factory_ = None
    _id_factory_: IdFactory = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def configure(self, configuration: ModelConfiguration):
        self._id_factory_ = configuration.floor_controllers_id_factory
        self._receivers_factory_ = configuration.call_receivers_factory

    def get_controllers_for(self, floor: int) -> FloorControllers:
        controllers = dict()
        for receiver in self._receivers_factory_.get_call_receivers_for(floor):
            controller_id = self._id_factory_.new_id()
            controllers.update({controller_id: FloorController(controller_id, floor=floor, receiver=receiver)})
        return FloorControllers(controllers)
