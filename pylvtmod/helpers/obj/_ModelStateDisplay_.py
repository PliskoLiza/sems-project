from pylvtmod import *


class ModelStateDisplay(ModelPostConfigurableObject, ModelLiveObject):

    def tick(self, time):
        pass

    def setup(self, model: Model):
        model.tick_actions.append(self)
