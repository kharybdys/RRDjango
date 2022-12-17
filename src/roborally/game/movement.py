from typing import Optional

from roborally.game import card
from roborally.models import Direction

TYPE_ROBOT = 'ROBOT'
TYPE_DUAL_CONVEYOR = 'DUAL_CONVEYOR'
TYPE_SINGLE_CONVEYOR = 'SINGLE_CONVEYOR'
TYPE_PUSHER = 'PUSHER'
TYPE_ROTATOR = 'ROTATOR'

CARD_U_TURN = 'U_TURN'
CARD_ROTATE_LEFT = 'ROTATE_LEFT'
CARD_ROTATE_RIGHT = 'ROTATE_RIGHT'
CARD_BACKUP = 'BACKUP'
CARD_MOVE1 = 'MOVE1'
CARD_MOVE2 = 'MOVE2'
CARD_MOVE3 = 'MOVE3'

MOVEMENT_CARD_TYPES = {CARD_U_TURN: (0, 2),
                       CARD_ROTATE_LEFT: (0, -1),
                       CARD_ROTATE_RIGHT: (0, 1),
                       CARD_BACKUP: (-1, 0),
                       CARD_MOVE1: (1, 0),
                       CARD_MOVE2: (2, 0),
                       CARD_MOVE3: (3, 0)
                       }

DIRECTIONS = {Direction.NORTH: 0, Direction.EAST: 1, Direction.SOUTH: 2, Direction.WEST: 3}


def get_turns(from_direction, to_direction):
    return DIRECTIONS[to_direction] - DIRECTIONS[from_direction]


def get_to_direction(from_direction: Optional[Direction], turns: int) -> Optional[Direction]:
    if from_direction:
        to_direction_int = (DIRECTIONS[from_direction] + turns) % 4
        result = None
        for (key, value) in DIRECTIONS.items():
            if value == to_direction_int:
                result = key
        if result is None:
            raise Exception(f'Trouble calculating to_direction based on {from_direction} and {turns}')
        return result
    else:
        return None


class Movement:

    def __init__(self, direction, card_definition):
        self.direction = direction
        self.steps, self.turns = MOVEMENT_CARD_TYPES[card.card_type(card_definition)]
        self.priority = card.priority(card_definition)
        self.type = TYPE_ROBOT
        self.validate()

    def __init__(self, direction, steps, turns, priority, movement_type):
        self.direction = direction
        self.steps = steps
        self.turns = turns
        self.priority = priority
        self.type = movement_type
        self.validate()

    def validate(self):
        assert self.steps == 0 or self.steps == 1
        assert self.steps == 0 or self.turns == 0
