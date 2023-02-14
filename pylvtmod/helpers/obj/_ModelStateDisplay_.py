from tabulate import tabulate, SEPARATING_LINE
from itertools import groupby
from clrscr import clrscr

from pylvtmod import *


class ModelStateDisplay(ModelPostConfigurableObject, ModelLiveObject):

    _model_: Model = None
    _delay_condition_ = None

    def __init__(self, *, delay: int = None, delay_condition = None):
        if delay_condition is not None:
            self._delay_condition_ = delay_condition
        elif delay is None:
            self._delay_condition_ = lambda _: True
        else:
            self._delay_condition_ = lambda time: time % delay == 0

    def tick(self, time, ticks):
        if self._delay_condition_(time):
            clrscr()
            self.display_state()

    def setup(self, model: Model):
        self._model_ = model
        model.tick_actions.append(self)
        self._max_num_len_ = len(str(model.building.floors.count()))

    _max_num_len_: int = None

    def display_state(self):
        self._display_parameters()
        self._display_building()
        self._display_lifts()

    def _display_parameters(self):
        self._display_block(
            "parameters",
            tabulate(
                [
                    [self._model_.time(), "Model time"],
                    [self._model_.ticks(), "Ticks from start"]
                ],
                colalign=['right', 'left'],
                tablefmt='plain'))

    def _display_building(self):
        self._display_block(
            "building",
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
                tablefmt='plain'))

    def _display_lifts(self):
        self._display_block(
            "lifts",
            tabulate(
                [SEPARATING_LINE] + [
                    [
                        cabin.cabin_id,
                        cabin.position.floor,
                        cabin.blocked(),
                        '-' if cabin.active_command() is None else
                        f"[ → #{cabin.active_command().target_floor}"
                        f"{' / E' if cabin.active_command().exchange_needed else ''}]",
                        ' '.join(f"[ #{floor} ← "
                                 f"{', '.join(map(lambda passenger: f'#{passenger.passenger_id}', passengers))} ]"
                                 for floor, passengers
                                 in groupby(cabin.passengers, key=lambda passenger: passenger.ticket.destination_floor))
                     ]
                    for cabin in self._model_.building.lifts.values()
                ],
                headers=["Cabin", "Floor", "Blocked", "Command", "Passengers"],
                colalign=['center', 'center', "center", 'center', 'left'],
                tablefmt='plain'))

    @staticmethod
    def _display_block(name, data):
        print(name.upper())
        print()

        for line in str(data).split('\n'):
            print("┃ " + line)

        print(end='\n\n')
