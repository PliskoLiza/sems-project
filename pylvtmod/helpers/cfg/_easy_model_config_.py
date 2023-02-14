from typing import Dict, Any, Iterable, List, Collection

from pylvtmod import *


def build_config(*,
                 floors_count: int,
                 floors_height: float,
                 first_floor_number: int = 1,

                 cabin_speed: float,
                 cabin_capacity: int,

                 cabins_load_ticks: int = None,
                 cabins_unload_ticks: int = None,
                 cabins_exchange_ticks: int = None,

                 cabins_count: int = None,
                 cabins_starts: Collection[LiftCabinPosition] = None,
                 cabins_start_floor: int = 1,

                 universal_receiver=None,
                 call_receiver: CallReceiver = None,
                 request_receiver: RequestReceiver = None,

                 tickets_factory: TicketsFactory = None,
                 flagging_provider: FlaggingProvider = None,

                 passengers_data_collector: PassengersDataCollector = None,

                 **additional_params):

    factory = _UniversalFactory(floors_count=floors_count,
                                floors_height=floors_height,
                                first_floor_number=first_floor_number,
                                cabin_speed=cabin_speed,
                                cabin_capacity=cabin_capacity,
                                cabins_count=cabins_count,
                                cabins_load_ticks=cabins_load_ticks,
                                cabins_unload_ticks=cabins_unload_ticks,
                                cabins_exchange_ticks=cabins_exchange_ticks,
                                cabins_starts=cabins_starts,
                                cabins_start_floor=cabins_start_floor,
                                universal_receiver=universal_receiver,
                                call_receiver=call_receiver,
                                request_receiver=request_receiver)

    return ModelConfiguration(tickets_factory=tickets_factory,
                              flagging_provider=flagging_provider,
                              passengers_data_collector=passengers_data_collector,
                              floor_plans_factory=factory,
                              call_receivers_factory=factory,
                              request_receivers_factory=factory,
                              lift_cabin_positions_factory=factory,
                              lift_cabin_specifics_factory=factory,
                              **additional_params)


class _UniversalFactory(FloorPlansFactory,
                        CallReceiversFactory,
                        RequestReceiversFactory,
                        LiftCabinPositionsFactory,
                        LiftCabinSpecificsFactory):

    floors_count: int = None
    floors_height: float = None
    first_floor_number: int = None

    cabin_speed: float = None
    cabin_capacity: int = None

    cabins_load_ticks: int = None
    cabins_unload_ticks: int = None

    cabins_count: int = None
    cabins_starts: Collection[LiftCabinPosition] = None
    cabins_start_floor: int = None

    call_receiver: CallReceiver = None
    request_receiver: RequestReceiver = None

    tickets_factory: TicketsFactory = None
    flagging_provider: FlaggingProvider = None

    passengers_data_collector: PassengersDataCollector = None

    def __init__(self, *,
                 floors_count: int,
                 floors_height: float,
                 first_floor_number: int = 1,

                 cabin_speed: float,
                 cabin_capacity: int,

                 cabins_load_ticks: int = None,
                 cabins_unload_ticks: int = None,
                 cabins_exchange_ticks: int = None,

                 cabins_count: int = None,
                 cabins_starts: Collection[LiftCabinPosition] = None,
                 cabins_start_floor: int = 1,

                 universal_receiver=None,
                 call_receiver: CallReceiver = None,
                 request_receiver: RequestReceiver = None):

        self.floors_count = floors_count
        self.floors_height = floors_height
        self.first_floor_number = first_floor_number

        self.cabin_speed = cabin_speed
        self.cabin_capacity = cabin_capacity

        self.cabins_load_ticks = cabins_load_ticks if cabins_load_ticks is not None else cabins_exchange_ticks
        self.cabins_unload_ticks = cabins_unload_ticks if cabins_unload_ticks is not None else cabins_exchange_ticks

        self.cabins_count = cabins_count if cabins_count is not None else len(cabins_starts)
        self.cabins_starts = cabins_starts
        self.cabins_start_floor = cabins_start_floor

        self.call_receiver = universal_receiver if universal_receiver is not None else call_receiver
        self.request_receiver = universal_receiver if universal_receiver is not None else request_receiver

    def build_configuration(self, **kwargs) -> ModelConfiguration:
        return ModelConfiguration(tickets_factory=self.tickets_factory,
                                  flagging_provider=self.flagging_provider,
                                  passengers_data_collector=self.passengers_data_collector,
                                  floor_plans_factory=self,
                                  call_receivers_factory=self,
                                  request_receivers_factory=self,
                                  lift_cabin_positions_factory=self,
                                  lift_cabin_specifics_factory=self,
                                  **kwargs)

    def get_floors_count(self) -> int:
        return self.floors_count

    def get_first_floor_number(self) -> int:
        return self.first_floor_number

    def get_floor_plans(self) -> List[FloorPlan]:
        return [FloorPlan(height=self.floors_height) for _ in range(0, self.floors_count)]

    def get_call_receivers_for(self, floor: int) -> Iterable[CallReceiver]:
        return (self.call_receiver for _ in range(0, self.cabins_count))

    def get_request_receivers(self) -> Dict[Any, RequestReceiver]:
        return {cabin_id: self.request_receiver for cabin_id in range(0, self.cabins_count)}

    def get_cabins_positions(self) -> Dict[Any, LiftCabinPosition]:
        return self.cabins_starts if self.cabins_starts is not None \
            else {cabin_id: LiftCabinPosition(floor=self.cabins_start_floor)
                  for cabin_id in range(0, self.cabins_count)}

    def get_cabins_specifics(self) -> Dict[Any, LiftCabinSpecific]:
        return {cabin_id: LiftCabinSpecific(speed=self.cabin_speed,
                                            capacity=self.cabin_capacity,
                                            load_ticks=self.cabins_load_ticks,
                                            unload_ticks=self.cabins_unload_ticks)
                for cabin_id in range(0, self.cabins_count)}
