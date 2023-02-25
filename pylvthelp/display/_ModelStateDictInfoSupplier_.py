from abc import ABCMeta
from tabulate import tabulate

from . import ModelStateInfoSupplier


class ModelStateDictInfoSupplier(ModelStateInfoSupplier, metaclass=ABCMeta):

    def get_info_str(self, time, ticks) -> str:
        return tabulate(map(lambda item: [item[1], item[0]], self.get_info(time, ticks).items()),
                        colalign=['right', 'left'], tablefmt='plain')
