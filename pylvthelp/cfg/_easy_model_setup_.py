from itertools import chain
from typing import Iterable

from pylvtmod import *


def setup_model(model: Model, *objects, scan_config: bool = True):
    for obj in (objects if not scan_config else chain(_scan_model_config(model), objects)):
        obj.setup(model)


def _scan_model_config(model: Model) -> Iterable[ModelPostConfigurableObject]:
    return filter(lambda obj: isinstance(obj, ModelPostConfigurableObject),
                  {model.configuration.__getattribute__(attr) for attr in
                   filter(lambda name: not name.startswith('_'),
                          dir(model.configuration))})
