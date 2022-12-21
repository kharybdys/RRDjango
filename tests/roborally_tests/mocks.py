from dataclasses import dataclass

from roborally.game.direction import Direction


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
    order_number: int

    def save(self):
        pass
