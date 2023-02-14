import os

import pylvtmod as md
from pylvtmod.helpers.cfg import build_config, setup_model
from pylvtmod.helpers.obj import UpDownFlaggingProvider, ModelStateDisplay

from spawners.SimpleSpawner import SimpleSpawner
from controllers.DumpController import DumpController


DURATION = 180

DISPLAY_DELAY = 180

CONFIG = build_config(

    floors_count=5,
    floors_height=3,
    first_floor_number=1,

    cabins_count=1,
    cabin_speed=0.1,
    cabin_capacity=4,
    cabins_start_floor=1,
    cabins_exchange_ticks=5,

    universal_receiver=DumpController(),
    tickets_factory=SimpleSpawner(),
    flagging_provider=UpDownFlaggingProvider()
)


if __name__ == '__main__':

    model = md.Model(configuration=CONFIG)
    setup_model(model, ModelStateDisplay(delay=DISPLAY_DELAY))

    model.run(condition=lambda m: m.time() < DURATION)
