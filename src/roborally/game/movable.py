from abc import ABC, abstractmethod

from roborally.board.basic import Point
from roborally.game.direction import Direction
from roborally.utils.codec import SerializationMixin


class Movable(ABC, SerializationMixin):
    PUSHABLE = True
    PUSHES = True
    HAS_DIRECTION = True

    def __init__(self):
        self.died_this_turn = False

    @abstractmethod
    def to_data(self) -> dict:
        pass

    @property
    @abstractmethod
    def coordinates(self) -> Point:
        pass

    @property
    def facing_direction(self) -> Direction:
        return Direction.NORTH

    @property
    @abstractmethod
    def order_number(self) -> int:
        pass

    @abstractmethod
    def update_coordinates_and_direction(self, new_coordinates: Point, new_direction: Direction):
        pass

    @abstractmethod
    def get_movements_for(self, round: int, phase: int) -> list["Movement"]:
        pass
