from typing import Self

from roborally.game.movable import Movable
from roborally.game.direction import Direction
from roborally.game.movement import Movement
from roborally.utils.codec import SerializationMixin

# parameters for drawing a board on the web
DRAW_MAGNIFICATION_FACTOR = 6


class BasicElement(SerializationMixin):
    KEY_ELEMENT_TYPE = 'element_type'
    KILLS = False

    def __init__(self):
        self.neighbours = {}
        self.walls: dict[Direction, bool] = {}

    def to_data(self) -> dict:
        return {self.KEY_ELEMENT_TYPE: self.__class__.__name__}

    # to be overridden, but a basic element simply does nothing
    def board_movements(self, phase: int, movable: Movable) -> Movement | None:
        return None

    def get_neighbour(self, direction: Direction) -> Self:
        return self.neighbours.get(direction)

    def set_neighbour(self, direction: Direction, element: Self):
        self.neighbours[direction] = element

    def neighbours_completed(self):
        pass

    def has_wall(self, direction: Direction) -> bool:
        return self.walls.get(direction, False)

    def set_wall(self, direction: Direction, wall: bool = True):
        self.walls[direction] = wall


class StartingElement(BasicElement):

    def __init__(self, symbol):
        super().__init__()
        self._symbol = symbol

    def to_data(self):
        element_data = super().to_data()
        element_data[self.KEY_SYMBOL] = self._symbol
        return element_data


class RepairElement(BasicElement):
    pass


class OptionElement(BasicElement):
    pass


class HoleElement(BasicElement):
    KILLS = True


class VoidElement(BasicElement):
    KILLS = True

    def to_data(self):
        raise Exception("Void elements cannot be serialized")
