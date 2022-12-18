from typing import Self

from roborally.game.card import CardDefinition

TYPE_ROBOT = 'ROBOT'
TYPE_DUAL_CONVEYOR = 'DUAL_CONVEYOR'
TYPE_SINGLE_CONVEYOR = 'SINGLE_CONVEYOR'
TYPE_PUSHER = 'PUSHER'
TYPE_ROTATOR = 'ROTATOR'


class Movement:

    def __init__(self, direction, steps, turns, priority, movement_type):
        self.direction = direction
        self.steps = steps
        self.turns = turns
        self.priority = priority
        self.type = movement_type
        self.validate()

    @classmethod
    def from_card_definition(cls, direction, card_definition: CardDefinition) -> list[Self]:
        card_type = card_definition.get_type()
        priority = card_definition.get_priority()
        steps = card_type.get_steps()
        turns = card_type.get_turns()
        # Manipulation to split into multiple movement objects if necessary
        if steps < 0:
            direction = direction.turn(2)
            steps = -steps
        actual_steps = 0 if steps == 0 else 1
        return [cls(direction, actual_steps, turns, priority, TYPE_ROBOT) for _ in range(0, min(steps, 1))]

    def validate(self):
        assert self.steps == 0 or self.steps == 1
        assert self.steps == 0 or self.turns == 0
