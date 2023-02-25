from typing import Union, Iterable, Any, Dict

from .. import ModelStateDictInfoSupplier


class ModelParametersInfoSupplier(ModelStateDictInfoSupplier):

    def get_name(self, _, __) -> str:
        return 'parameters'

    def get_info(self, time, ticks) -> Union[str, Iterable[Any], Dict[Any, Any]]:
        return {'Model time': time, 'Ticks from start': ticks}
