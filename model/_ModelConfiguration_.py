from . import IdFactory, IntIdFactory
from . import TimeCounter, SimpleTimeCounter
from . import FlaggingProvider, CallReceiversFactory, TicketsFactory


class ModelConfiguration:

    floors_count: int = None
    time_counter: TimeCounter = None
    tickets_factory: TicketsFactory = None
    passengers_id_factory: IdFactory = None
    flagging_provider: FlaggingProvider = None
    call_receivers_factory: CallReceiversFactory = None
    floor_controllers_id_factory: IdFactory = None

    def __init__(self, *,
                 floors_count: int,
                 tickets_factory: TicketsFactory,
                 flagging_provider: FlaggingProvider,
                 call_receivers_factory: CallReceiversFactory,
                 time_counter: TimeCounter = SimpleTimeCounter(),
                 passengers_id_factory: IdFactory = IntIdFactory(),
                 floor_controllers_id_factory: IdFactory = IntIdFactory()):

        self.floors_count = floors_count
        self.time_counter = time_counter
        self.tickets_factory = tickets_factory
        self.flagging_provider = flagging_provider
        self.passengers_id_factory = passengers_id_factory
        self.call_receivers_factory = call_receivers_factory
        self.floor_controllers_id_factory = floor_controllers_id_factory
