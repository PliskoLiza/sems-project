from enum import Flag


class LiftCabinState(Flag):                         # BitFlag

    MovingUP = int('10000', 2)                      # 10000
    MovingDOWN = int('00001', 2)                    # 00001

    Moving = MovingUP | MovingDOWN                  # 10001
    Parked = int('00100', 2)                        # 00100

    _exchange = int('01000', 2)                     # 01000
    _freeze = int('00010', 2)                       # 00010

    UnderEXCHANGE = Parked | _exchange              # 01100
    _UnderFREEZE = Parked | _freeze                 # 00110

    AVAILABLE = Parked | MovingUP | MovingDOWN      # 10101
    BLOCKED = _exchange | _freeze                   # 01010

    @staticmethod
    def get_state_sign(state):

        if state == LiftCabinState.Parked:
            return '-'
        elif state == LiftCabinState.UnderEXCHANGE:
            return 'E'
        elif state == LiftCabinState.MovingUP:
            return '↑'
        elif state == LiftCabinState.MovingDOWN:
            return '↓'

        return bin(state)
