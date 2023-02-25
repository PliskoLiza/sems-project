import random as rnd
from typing import Iterable

import pylvtmod as md
from pylvtmod import Ticket, Model


class SimpleSpawner(md.TicketsFactory, md.ModelPostConfigurableObject):

    _floors_count_: int = None

    _up_interval_ = None
    _down_interval_ = None

    _up_random_ = None
    _down_random_ = None

    _start_: bool = None
    _down_next_ = None
    _up_next_ = None

    _up_group_max_: int = None
    _up_group_min_: int = None
    _down_group_max_: int = None
    _down_group_min_: int = None

    _cutoff_ = None

    def __init__(self, *, cutoff=None,
                 up_interval, down_interval,
                 up_group_min: int = 1, down_group_min: int = 1,
                 up_group_max: int = 1, down_group_max: int = 1,
                 up_random: int = None, down_random: int = None):

        self._cutoff_ = cutoff

        self._up_interval_ = up_interval
        self._down_interval_ = down_interval

        self._up_random_ = up_random
        self._down_random_ = down_random

        self._up_group_min_ = up_group_min
        self._up_group_max_ = up_group_max
        self._down_group_min_ = down_group_min
        self._down_group_max_ = down_group_max

    def setup(self, model: Model):
        self._floors_count_ = model.building.floors.count()
        self._start_ = True

    def generate_tickets(self, time, ticks) -> Iterable[Ticket]:

        if time <= self._cutoff_:

            if self._start_:
                self._up_next_ = self._get_next_time(time, self._up_interval_, self._up_random_)
                self._down_next_ = self._get_next_time(time, self._down_interval_, self._down_random_)
                self._start_ = False

            if time == self._up_next_:
                self._up_next_ = self._get_next_time(time, self._up_interval_, self._up_random_)
                return [md.Ticket(departure=1, destination=rnd.randint(2, self._floors_count_))
                        for _ in range(rnd.randint(self._up_group_min_, self._up_group_max_))]

            if time == self._down_next_:
                self._down_next_ = self._get_next_time(time, self._down_interval_, self._down_random_)
                return [md.Ticket(departure=rnd.randint(2, self._floors_count_), destination=1)
                        for _ in range(rnd.randint(self._down_group_min_, self._down_group_max_))]

        return []

    @staticmethod
    def _get_next_time(current, interval, random):
        return current + interval + (0 if random is None else rnd.randint(-random, random))
