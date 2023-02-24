from abc import abstractmethod

from . import Model


class ModelPostConfigurableObject:

    @abstractmethod
    def setup(self, model: Model):
        pass
