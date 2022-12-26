from dataclasses import dataclass

from roborally.game.direction import Direction
from roborally_tests.game.events import TestEventHandler


@dataclass
class Coordinates:
    x_coordinate: int
    y_coordinate: int


@dataclass
class CoordinatesWithDirection(Coordinates):
    facing_direction: Direction


@dataclass
class FlagModelMock(Coordinates):
    order_number: int

    def save(self):
        pass


@dataclass
class BotModelMock(CoordinatesWithDirection):
    order_number: int = 0

    def save(self):
        pass


@dataclass
class Expectation(CoordinatesWithDirection):
    event_handler: TestEventHandler = None
