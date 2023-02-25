from typing import Any, Union, Iterable, Callable, Tuple
from tabulate import tabulate, SEPARATING_LINE
from itertools import groupby
from clrscr import clrscr
from time import sleep

from pylvtmod import *
from .. import ModelStateInfoSupplier


class ConsoleModelStateDisplay(ModelPostConfigurableObject, ModelLiveObject):

    BUILDING_SHOW = 'BUILDING_BLOCK'

    _model_: Model = None

    _interval_condition_ = None
    _display_delay_: float = None

    _display_map_: Union[Iterable[Union[Tuple[str, str], Callable[[Any, Any], Tuple[str, str]], ModelStateInfoSupplier]],
                         Iterable[Callable[[Any, Any], Tuple[str, str]]]] = None

    def __init__(self, display_map: Iterable = None,
                 interval_ticks: int = None, interval_condition=None, display_delay: float = None):

        self._display_delay_ = display_delay

        if interval_condition is not None:
            self._interval_condition_ = interval_condition
        elif interval_ticks is None:
            self._interval_condition_ = lambda _, __: True
        else:
            self._interval_condition_ = lambda _, ticks: ticks % interval_ticks == 0

        display_map = [self.BUILDING_SHOW] if display_map is None else display_map
        self._display_map_: list = [(point if point != self.BUILDING_SHOW
                                     else lambda time, ticks: ('building', self.get_building_show(time, ticks)))
                                    for point in display_map]

    def setup(self, model: Model):

        self._model_ = model

        for point in self._display_map_:
            if isinstance(point, ModelPostConfigurableObject):
                point.setup(model)

        self._display_map_ = self._form_display_map(self._display_map_)
        model.tick_actions.append(self)

    @staticmethod
    def _form_display_map(pattern):

        def get_func(name_getter, data_getter):
            return lambda time, ticks: (name_getter(time, ticks), data_getter(time, ticks))

        return [
            ((lambda _, __: point) if type(point) is tuple
             else get_func(point.get_name, point.get_info_str)
             if isinstance(point, ModelStateInfoSupplier)
             else point)
            for point in pattern
        ]

    def tick(self, time, ticks):
        if self._interval_condition_(time, ticks):
            clrscr()
            self.display_state(time, ticks)
            self._delay()

    def _delay(self):
        if self._display_delay_ is not None:
            sleep(self._display_delay_)

    def display_state(self, time, ticks):
        for block in self._display_map_:
            info = block(time, ticks)
            self._display_block(*info)

    @staticmethod
    def _display_block(name, data):
        print(name.upper())
        print()

        for line in str(data).split('\n'):
            print("┃ " + line)

        print(end='\n\n')

    def get_building_show(self, time, ticks):
        return \
            tabulate(
                [SEPARATING_LINE] + [
                    [
                        floor.number,
                        '  '.join('█' if cabin.position.floor == floor.number else '│'
                                  for cabin in self._model_.building.lifts.values()),
                        '  '.join(self._model_.configuration.flagging_provider.get_flag_sign(controller.state)
                                  for controller in floor.controllers),
                        ' '.join(f'[ ' + ('+' if floor.controllers.state_exists(flag) else '-') + ' / ' +
                                 f"{self._model_.configuration.flagging_provider.get_flag_sign(flag)} / " +
                                 ', '.join(map(lambda waiter: f'#{waiter.passenger.passenger_id}', floor.queue)) + ' ]'
                                 for flag, waiters in groupby(floor.queue, key=lambda waiter: waiter.flag))
                     ]
                    for floor in self._model_.building.floors.reversed()
                ],
                headers=["Floor", "Cabins", "Controllers", "Waiters"],
                colalign=['center', 'center', 'center', 'left'],
                tablefmt='plain')
