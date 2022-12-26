from dataclasses import dataclass

from roborally.board.basic import Point
from roborally.game.basic import Movable
from roborally.game.direction import Direction


@dataclass
class Coordinates:
    x_coordinate: int
    y_coordinate: int


@dataclass
class CoordinatesWithDirection(Coordinates):
    facing_direction: Direction


@dataclass
@dataclass
class MovableModelMock(CoordinatesWithDirection):
    order_number: int = 0

    def save(self):
        pass


@dataclass
class Expectation(CoordinatesWithDirection):
    movable: Movable

    def verify(self):
        assert self.movable.coordinates.x == self.x_coordinate
        assert self.movable.coordinates.y == self.y_coordinate
        # TODO: Shouldn't depend on PUSHES
        if self.movable.HAS_DIRECTION:
            assert self.movable.facing_direction == self.facing_direction
