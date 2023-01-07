from abc import ABC, abstractmethod

from roborally.board.basic import Point
from roborally.game.card import CardDefinition
from roborally.game.direction import Direction
from roborally.game.events import PublishMixin
from roborally.utils.codec import SerializationMixin


class Movable(ABC, SerializationMixin, PublishMixin):
    DEFAULT_DIRECTION = Direction.NORTH
    PUSHABLE = True
    PUSHES = True
    HAS_DIRECTION = True
    KEY_TYPE = "movable_type"

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
    @abstractmethod
    def archive_coordinates(self) -> Point:
        pass

    @property
    def facing_direction(self) -> Direction:
        return Movable.DEFAULT_DIRECTION

    @property
    @abstractmethod
    def order_number(self) -> int:
        pass

    @property
    @abstractmethod
    def damage(self) -> int:
        pass

    @abstractmethod
    def update_coordinates_and_direction(self, new_coordinates: Point, new_direction: Direction):
        pass

    @abstractmethod
    def get_cards_for(self, round: int, phase: int) -> list[CardDefinition]:
        pass

    @abstractmethod
    def take_damage(self, damage: int):
        pass

    def cleanup_killed_at_model(self):
        pass

    def process_killed(self, phase: int, by_board: bool = False):
        if by_board:
            self.log_killed_by_hole(phase)
        else:
            self.log_killed_by_damage(phase)
        self.died_this_turn = True
        self.update_coordinates_and_direction(Point(-100, -100), Movable.DEFAULT_DIRECTION)

    # After the round
    def cleanup_killed(self):
        self.died_this_turn = False
        self.update_coordinates_and_direction(self.archive_coordinates, Movable.DEFAULT_DIRECTION)
        self.cleanup_killed_at_model()
