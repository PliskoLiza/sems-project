from typing import Iterable, Any

import pylvtmod.helpers
import pylvtmod as md


class CustomController(md.CallReceiver, md.RequestReceiver):

    lifts = None

    def push_call(self, call: md.Call):
        pass

    def push_request(self, request: md.Request):
        pass


class CustomTicketsFactory(md.TicketsFactory):
    def generate_tickets(self, time) -> Iterable[md.Ticket]:
        pass


class CustomFlaggingProvider(md.FlaggingProvider):

    def get_all_flags(self) -> Iterable[Any]:
        return ['up', 'dn']

    def get_flag_for(self, ticket: md.Ticket) -> Any:
        return 'up' if ticket.destination_floor > ticket.departure_floor else 'dn'


config = md.helpers.SimpleModelConfigurator(
    floors_count=9,
    floors_height=300,
    cabins_count=1,
    cabin_speed=10,
    cabin_capacity=5,
    universal_receiver=CustomController(),
    tickets_factory=CustomTicketsFactory(),
    flagging_provider=CustomFlaggingProvider()
    ).build_configuration()

model = md.Model(configuration=config)
pass
