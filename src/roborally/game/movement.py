from dataclasses import dataclass
from typing import Self, Optional

from roborally.board.basic import Point
from roborally.game.basic import Movable
from roborally.game.bot import Bot
from roborally.game.card import CardDefinition
from roborally.game.direction import Direction
from roborally.game.events import EventHandler

TYPE_ROBOT = 'ROBOT'
TYPE_DUAL_CONVEYOR = 'DUAL_CONVEYOR'
TYPE_SINGLE_CONVEYOR = 'SINGLE_CONVEYOR'
TYPE_PUSHER = 'PUSHER'
TYPE_ROTATOR = 'ROTATOR'


class Movement:

    def __init__(self, direction: Optional[Direction], steps: int, turns: int, priority: int, movement_type: str, moved_object: Movable):
        self.direction = direction
        self.steps = steps
        self.turns = turns
        self.priority = priority
        self.type = movement_type
        self.moved_object = moved_object
        self.validate()

    @classmethod
    def from_card_definition(cls, bot: Bot, card_definition: CardDefinition) -> list[Self]:
        direction = bot.facing_direction
        card_type = card_definition.get_type()
        priority = card_definition.get_priority()
        steps = card_type.get_steps()
        turns = card_type.get_turns()
        # invert direction if negative steps
        if steps < 0:
            direction = direction.turn(2)
            steps = -steps
        actual_steps = 0 if steps == 0 else 1
        # Manipulation to split into multiple movement objects if necessary
        return [cls(direction, actual_steps, turns, priority, TYPE_ROBOT, bot) for _ in range(0, min(steps, 1))]

    def validate(self):
        assert self.steps == 0 or self.steps == 1
        assert self.direction is not None or self.steps == 0


@dataclass
class MovementPossibility:
    event_handler: EventHandler
    movable: Movable
    new_coordinates: Point
    new_direction: Direction

    @staticmethod
    def from_movable(event_handler: EventHandler, movable: Movable):
        return MovementPossibility(event_handler, movable, movable.coordinates, movable.facing_direction)

    def is_noop(self):
        return self.movable.coordinates == self.new_coordinates and self.movable.facing_direction == self.new_direction

    def cancel_if_target_coord_matches(self, duplicated_coordinates: Point) -> Self:
        if duplicated_coordinates == self.new_coordinates and not self.is_noop():
            self.event_handler.log_board_movement_impossible(self.movable)
            return MovementPossibility.from_movable(self.event_handler, self.movable)
        else:
            return self
