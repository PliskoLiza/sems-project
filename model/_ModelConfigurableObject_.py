from abc import abstractmethod

from . import ModelConfiguration


class ModelConfigurableObject:

    def __init__(self, *args, configuration: ModelConfiguration, **kwargs):
        self.configure(configuration)

    @abstractmethod
    def configure(self, configuration: ModelConfiguration):
        pass
