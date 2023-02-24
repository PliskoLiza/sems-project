from abc import abstractmethod


class IdFactory:

    @abstractmethod
    def new_id(self):
        pass
