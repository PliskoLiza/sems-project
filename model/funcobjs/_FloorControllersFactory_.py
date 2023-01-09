from typing import Any, Dict

from .. import ModelConfiguration
from .. import IdFactory
from . import FloorController


class FloorControllersFactory:

    _receivers_factory_ = None
    _id_factory_: IdFactory = None

    def __init__(self, *, configuration: ModelConfiguration):
        self.configure(configuration)

    def configure(self, configuration: ModelConfiguration):
        self._id_factory_ = configuration.floor_controllers_id_factory
        self._receivers_factory_ = configuration.call_receivers_factory

    def get_controllers_for(self, floor: int) -> Dict[Any, FloorController]:
        controllers = dict()
        for receiver in self._receivers_factory_.get_receivers_for(floor):
            controller_id = self._id_factory_.new_id()
            controllers.update({controller_id: FloorController(controller_id, floor=floor, receiver=receiver)})
        return controllers
