from dataclasses import dataclass, field

from roborally.game.card import CardDefinition
from roborally.game.events import EventType
from roborally.game.movable import Movable
from roborally.game.direction import Direction
from roborally_tests.game.events import EventChecker


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
    event_checker: EventChecker
    type: str
    order_number: int = 0
    movement_cards: list[MovementCardMock] = field(default_factory=list)

    def save(self):
        pass

    def log_event(self, phase: int, event_type: EventType, other: Movable = None, **kwargs):
        other_type = None
        other_order_nr = None
        if other and isinstance(other.model, MovableModelMock):
            other_type = other.model.type
            other_order_nr = other.model.order_number
        self.event_checker.log_event(phase, event_type, self.type, self.order_number, other_type, other_order_nr, **kwargs)

    def add_card(self, round, phase, status, card_definition):
        self.movement_cards.append(MovementCardMock(round, phase, status, card_definition))

    def get_cards_for(self, round, phase) -> list[CardDefinition]:
        return [CardDefinition(card.card_definition)
                for card
                in filter(lambda c: c.round == round and c.phase == phase and c.status in ['FINAL', 'LOCKED'], self.movement_cards)]


@dataclass
class Expectation(CoordinatesWithDirection):
    movable: Movable

    def verify(self):
        assert self.movable.coordinates.x == self.x_coordinate
        assert self.movable.coordinates.y == self.y_coordinate
        if self.movable.HAS_DIRECTION and self.facing_direction:
            assert self.movable.facing_direction == self.facing_direction
