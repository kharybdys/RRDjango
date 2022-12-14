from dataclasses import dataclass
from typing import Self, Optional

from roborally.board.basic import Point
from roborally.game.movable import Movable
from roborally.game.card import CardDefinition
from roborally.game.direction import Direction


class Movement:

    def __init__(self, direction: Optional[Direction], steps: int, turns: int, priority: int, can_push: bool, phase: int, moved_object: Movable):
        self.direction = direction
        self.steps = steps
        self.turns = turns
        self.priority = priority
        self.can_push = can_push
        self.phase = phase
        self.moved_object = moved_object
        self.validate()

    @classmethod
    def from_card_definition(cls, movable: Movable, phase: int, card_definition: CardDefinition) -> list[Self]:
        direction = movable.facing_direction
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
        return [cls(direction, actual_steps, turns, priority, True, phase, movable) for _ in range(0, max(steps, 1))]

    def validate(self):
        assert self.steps == 0 or self.steps == 1
        assert self.direction is not None or self.steps == 0


@dataclass
class MovementPossibility:
    phase: int
    movable: Movable
    new_coordinates: Point
    new_direction: Direction
    kills: bool = False

    @staticmethod
    def from_movable(phase: int, movable: Movable):
        return MovementPossibility(phase, movable, movable.coordinates, movable.facing_direction)

    def is_noop(self):
        return self.movable.coordinates == self.new_coordinates and self.movable.facing_direction == self.new_direction

    def cancel_if_target_coord_matches(self, duplicated_coordinates: Point) -> Self:
        if duplicated_coordinates == self.new_coordinates and not self.is_noop():
            self.movable.log_board_movement_impossible(self.phase)
            return MovementPossibility.from_movable(self.phase, self.movable)
        else:
            return self

    def process(self):
        if not self.is_noop():
            if self.kills:
                self.movable.process_killed(phase=self.phase, by_board=True)
            else:
                self.movable.update_coordinates_and_direction(self.new_coordinates, self.new_direction)
