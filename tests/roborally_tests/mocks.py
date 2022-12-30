from dataclasses import dataclass

from roborally.game.card import CardDefinition
from roborally.game.movable import Movable
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
        if self.movable.HAS_DIRECTION and self.facing_direction:
            assert self.movable.facing_direction == self.facing_direction
