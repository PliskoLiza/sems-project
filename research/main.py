import pylvtmod as md

from pylvthelp import build_config, setup_model
from pylvthelp import BasicPassengersStatsProvider
from pylvthelp import SimpleFlaggingProvider, ConsoleModelStateDisplay
from pylvthelp import ModelParametersInfoSupplier, DefaultCabinsInfoSupplier

from spawners.SimpleSpawner import SimpleSpawner
from controllers.DumpController import DumpController


DURATION = 10800

STATS_PROVIDER = BasicPassengersStatsProvider()

DISPLAY_DELAY = 1
DISPLAY_INTERVAL = 30
DISPLAY_PROVIDER = ConsoleModelStateDisplay(
    [
        ModelParametersInfoSupplier(),
        STATS_PROVIDER,
        ConsoleModelStateDisplay.BUILDING_SHOW,
        DefaultCabinsInfoSupplier(),
    ],
    interval_ticks=DISPLAY_INTERVAL, display_delay=DISPLAY_DELAY)

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
    tickets_factory=SimpleSpawner(cutoff=DURATION - 600,
                                  up_interval=180, down_interval=600,
                                  up_random=60, down_random=120,
                                  up_group_max=2, down_group_max=1),
    flagging_provider=SimpleFlaggingProvider(),

    passengers_data_collector=STATS_PROVIDER
)


def main():

    model = md.Model(configuration=CONFIG)
    setup_model(model, CONTROLLER, DISPLAY_PROVIDER)

    model.run(condition=lambda m: m.time() < DURATION)


if __name__ == '__main__':
    main()
