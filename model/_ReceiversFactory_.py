from abc import abstractmethod

from model._Floor_ import Floor


class ReceiversFactory:

    @abstractmethod
    def get_receivers_for(self, floor: Floor):
        pass
