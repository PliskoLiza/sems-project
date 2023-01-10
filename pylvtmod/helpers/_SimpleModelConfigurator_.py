from typing import Dict, Any, Iterable, List, Collection

from .. import *


class SimpleModelConfigurator(FloorPlansFactory,
                              CallReceiversFactory,
                              RequestReceiversFactory,
                              LiftCabinPositionsFactory,
                              LiftCabinSpecificsFactory):

    floors_count: int = None
    floors_height: int = None
    first_floor_number: int = None

    cabin_speed: float = None
    cabin_capacity: int = None

    cabins_count: int = None
    cabins_starts: Collection[LiftCabinPosition] = None
    cabins_start_floor: int = None

    call_receiver: CallReceiver = None
    request_receiver: RequestReceiver = None

    tickets_factory: TicketsFactory = None
    flagging_provider: FlaggingProvider = None

    def __init__(self, *,
                 floors_count: int,
                 floors_height: float,
                 first_floor_number: int = 1,

                 cabin_speed: float,
                 cabin_capacity: int,

                 cabins_count: int = None,
                 cabins_starts: Collection[LiftCabinPosition] = None,
                 cabins_start_floor: int = 1,

                 universal_receiver=None,
                 call_receiver: CallReceiver = None,
                 request_receiver: RequestReceiver = None,

                 tickets_factory: TicketsFactory = None,
                 flagging_provider: FlaggingProvider = None):

        self.floors_count = floors_count
        self.floors_height = floors_height
        self.first_floor_number = first_floor_number

        self.cabin_speed = cabin_speed
        self.cabin_capacity = cabin_capacity

        self.cabins_count = cabins_count if cabins_count is not None else len(cabins_starts)
        self.cabins_starts = cabins_starts
        self.cabins_start_floor = cabins_start_floor

        self.call_receiver = universal_receiver if universal_receiver is not None else call_receiver
        self.request_receiver = universal_receiver if universal_receiver is not None else request_receiver

        self.tickets_factory = tickets_factory
        self.flagging_provider = flagging_provider

    def build_configuration(self, **kwargs) -> ModelConfiguration:
        return ModelConfiguration(tickets_factory=self.tickets_factory,
                                  flagging_provider=self.flagging_provider,
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
        return {cabin_id: LiftCabinSpecific(speed=self.cabin_speed, capacity=self.cabin_capacity)
                for cabin_id in range(0, self.cabins_count)}
