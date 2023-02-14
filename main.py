import pylvtmod as md
from pylvtmod.helpers.cfg import build_config, setup_model
from pylvtmod.helpers.obj import SimpleFlaggingProvider, ModelStateDisplay

from spawners.SimpleSpawner import SimpleSpawner
from controllers.DumpController import DumpController


DURATION = 10800

DISPLAY_DELAY = 1
DISPLAY_INTERVAL = 30

CONTROLLER = DumpController()

CONFIG = build_config(

    floors_count=25,
    floors_height=3,
    first_floor_number=1,

    cabins_count=1,
    cabin_speed=0.25,
    cabin_capacity=10,
    cabins_start_floor=1,
    cabins_exchange_ticks=5,

    universal_receiver=CONTROLLER,
    tickets_factory=SimpleSpawner(),
    flagging_provider=SimpleFlaggingProvider()
)


if __name__ == '__main__':

    model = md.Model(configuration=CONFIG)
    setup_model(model, CONTROLLER, ModelStateDisplay(interval_ticks=DISPLAY_INTERVAL, display_delay=DISPLAY_DELAY))

    model.run(condition=lambda m: m.time() < DURATION)
