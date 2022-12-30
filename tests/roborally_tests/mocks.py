from dataclasses import dataclass, field

from roborally.game.card import CardDefinition
from roborally.game.movable import Movable
from roborally.game.direction import Direction
from roborally.game.movement import Movement


@dataclass
class MovementCardMock:
    round: int
    phase: int
    status: str
    card_definition: str


@dataclass
class Coordinates:
    x_coordinate: int
    y_coordinate: int


@dataclass
class CoordinatesWithDirection(Coordinates):
    facing_direction: Direction


@dataclass
class MovableModelMock(CoordinatesWithDirection):
    order_number: int = 0
    movement_cards: list[MovementCardMock] = field(default_factory=list)

    def save(self):
        pass

    def add_card(self, round, phase, status, card_definition):
        self.movement_cards.append(MovementCardMock(round, phase, status, card_definition))

    def get_movements_for(self, round, phase, movable) -> list[Movement]:
        return [movement
                for card
                in filter(lambda c: c.round == round and c.phase == phase and c.status in ['FINAL', 'LOCKED'], self.movement_cards)
                for movement
                in Movement.from_card_definition(movable, CardDefinition(card.card_definition))]


@dataclass
class Expectation(CoordinatesWithDirection):
    movable: Movable

    def verify(self):
        assert self.movable.coordinates.x == self.x_coordinate
        assert self.movable.coordinates.y == self.y_coordinate
        if self.movable.HAS_DIRECTION and self.facing_direction:
            assert self.movable.facing_direction == self.facing_direction
