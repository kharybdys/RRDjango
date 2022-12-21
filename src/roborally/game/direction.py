from enum import Enum
from typing import Optional, Self


class Direction(Enum):
    NORTH = 'NORTH'
    EAST = 'EAST'
    SOUTH = 'SOUTH'
    WEST = 'WEST'

    @classmethod
    def get_choices(cls):
        return [(key.value, key.name) for key in cls]

    def to_int(self):
        match self:
            case self.NORTH:
                return 0
            case self.EAST:
                return 1
            case self.SOUTH:
                return 2
            case self.WEST:
                return 3
            case _:
                raise ValueError(f"Unsupported direction {self}")

    def turns_to(self, to_direction: Self):
        return to_direction.to_int() - self.to_int() % 4

    def turn(self, turns: int):
        to_direction_int = (self.to_int() + turns) % 4
        for direction in list(Direction):
            if direction.to_int() == to_direction_int:
                return direction
        raise Exception(f'Trouble calculating to_direction based on {self} and {turns}')


def get_to_direction(from_direction: Optional[Direction], turns: int) -> Optional[Direction]:
    if from_direction:
        return from_direction.turn(turns)
    else:
        return None


def to_optional_direction(direction_name: Optional[str]) -> Optional[Direction]:
    if not direction_name:
        return None
    else:
        return Direction(direction_name)
