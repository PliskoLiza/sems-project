from . import IdFactory, IntIdFactory
from . import TimeCounter, SimpleTimeCounter
from . import PassengersDataCollector
from . import FlaggingProvider, CallReceiversFactory, RequestReceiversFactory, TicketsFactory
from . import FloorPlansFactory, LiftCabinSpecificsFactory, LiftCabinPositionsFactory


class ModelConfiguration:

    time_counter: TimeCounter = None
    tickets_factory: TicketsFactory = None
    passengers_id_factory: IdFactory = None
    flagging_provider: FlaggingProvider = None
    floor_plans_factory: FloorPlansFactory = None
    passengers_data_collector: PassengersDataCollector = None
    lift_cabin_specifics_factory: LiftCabinSpecificsFactory = None
    lift_cabin_positions_factory: LiftCabinPositionsFactory = None
    request_receivers_factory: RequestReceiversFactory = None
    call_receivers_factory: CallReceiversFactory = None
    floor_controllers_id_factory: IdFactory = None

    def __init__(self, *,
                 tickets_factory: TicketsFactory,
                 flagging_provider: FlaggingProvider,
                 floor_plans_factory: FloorPlansFactory,
                 call_receivers_factory: CallReceiversFactory,
                 request_receivers_factory: RequestReceiversFactory,
                 lift_cabin_specifics_factory: LiftCabinSpecificsFactory,
                 lift_cabin_positions_factory: LiftCabinPositionsFactory,
                 time_counter: TimeCounter = SimpleTimeCounter(),
                 passengers_id_factory: IdFactory = IntIdFactory(),
                 floor_controllers_id_factory: IdFactory = IntIdFactory(),
                 passengers_data_collector: PassengersDataCollector = None):

        self.time_counter = time_counter
        self.tickets_factory = tickets_factory
        self.flagging_provider = flagging_provider
        self.floor_plans_factory = floor_plans_factory
        self.passengers_id_factory = passengers_id_factory
        self.call_receivers_factory = call_receivers_factory
        self.request_receivers_factory = request_receivers_factory
        self.passengers_data_collector = passengers_data_collector
        self.lift_cabin_specifics_factory = lift_cabin_specifics_factory
        self.lift_cabin_positions_factory = lift_cabin_positions_factory
        self.floor_controllers_id_factory = floor_controllers_id_factory
