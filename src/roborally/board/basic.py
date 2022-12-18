from dataclasses import dataclass
from typing import Self, ClassVar

from roborally.game.direction import Direction
from roborally.utils.codec import SerializationMixin


@dataclass
class Point(SerializationMixin):
    x: int
    y: int

    KEY_X: ClassVar[str] = 'x'
    KEY_Y: ClassVar[str] = 'y'

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def __le__(self, other):
        return self.y < other.y or (self.y == other.y and self.x <= other.x)

    def neighbour(self, direction: Direction) -> Self:
        """
            Defines the relation between the coordinate system and the directions
            0,0 will be top-left as that is what fabric.js expects
        """
        match direction:
            case Direction.SOUTH:
                return Point(self.x, self.y + 1)
            case Direction.NORTH:
                return Point(self.x, self.y - 1)
            case Direction.WEST:
                return Point(self.x - 1, self.y)
            case Direction.EAST:
                return Point(self.x + 1, self.y)

    def to_data(self) -> dict:
        return {self.KEY_X: self.x, self.KEY_Y: self.y}
