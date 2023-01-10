from typing import Iterable

import pylvtmod.helpers
import pylvtmod as md


class CustomTicketsFactory(md.TicketsFactory):
    def generate_tickets(self, time) -> Iterable[md.Ticket]:
        pass


class CustomController(md.helpers.LiveLiftController):
    def tick(self, time):
        pass


def main(duration: int):
    controller = CustomController()
    config = md.helpers.SimpleModelConfigurator(
        floors_count=9,
        floors_height=300,
        cabins_count=1,
        cabin_speed=10,
        cabin_capacity=5,
        universal_receiver=CustomController(),
        tickets_factory=CustomTicketsFactory(),
        flagging_provider=md.helpers.UpDownFlaggingProvider()
    ).build_configuration()

    model = md.Model(configuration=config)
    controller.setup(model)

    model.run(lambda env: env.time() < duration)
    pass


if __name__ == '__main__':
    main(3600)
