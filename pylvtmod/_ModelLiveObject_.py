from abc import abstractmethod


class ModelLiveObject:

    @abstractmethod
    def tick(self, time, ticks):
        pass
