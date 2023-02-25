from typing import Union, Iterable, Any, Dict
from tabulate import tabulate, SEPARATING_LINE
from itertools import groupby, chain

from pylvtmod import *
from .. import ModelStateInfoSupplier


class DefaultCabinsInfoSupplier(ModelPostConfigurableObject, ModelStateInfoSupplier):

    _lifts_: Dict[Any, LiftCabin] = None

    def setup(self, model: Model):
        self._lifts_ = model.building.lifts

    def get_name(self, _, __) -> str:
        return 'elevators'

    def get_info(self, time, ticks) -> Union[str, Iterable[Any], Dict[Any, Any]]:
        return {cabin.cabin_id:
                    {
                        'Floor': cabin.position.floor,
                        'Blocked': cabin.blocked(),
                        'Command': '-' if cabin.active_command() is None else
                                   f"[ → #{cabin.active_command().target_floor}"
                                   f"{f' / E' if cabin.active_command().exchange_needed else ''} ]",
                        'Filling': f"{cabin.passnumber} / {cabin.specific.capacity}",
                        'Passengers': ' '.join(f"[ #{floor} ← "
                                      f"{', '.join(map(lambda passenger: f'#{passenger.passenger_id}', passengers))} ]"
                                      for floor, passengers
                                      in groupby(cabin.passengers,
                                                 key=lambda passenger: passenger.ticket.destination_floor))
                    }
                for cabin in self._lifts_.values()}

    def get_info_str(self, time, ticks) -> str:

        info: dict = self.get_info(time, ticks)
        table = {key: [SEPARATING_LINE] for key in chain(['Cabin'], info[next(iter((info.keys())))].keys())}

        for cabin_id, cabin_info in info.items():
            table['Cabin'].append(cabin_id)
            for column in cabin_info.keys():
                table[column].append(cabin_info[column])

        return tabulate(table,
                        headers='keys',
                        colalign=['center', 'center', "center", 'center', 'center',  'left'],
                        tablefmt='plain')
