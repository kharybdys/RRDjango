import pytest

from roborally.game.direction import Direction
from roborally.game.movement import Movement
from roborally_tests.game.data import to_dummy_movable


def test_create_movement_steps():
    # steps beyond -1000 or +1000 mean you're stepping off the board anyway
    for steps in [*range(-1000, -1), *range(2, 1000)]:
        with pytest.raises(AssertionError):
            Movement(steps=steps,
                     turns=0,
                     priority=0,
                     direction=Direction.SOUTH,
                     can_push=True,
                     phase=1,
                     moved_object=to_dummy_movable(0, 0, Direction.NORTH))


def test_create_movement_steps_has_direction():
    with pytest.raises(AssertionError):
        Movement(steps=1,
                 turns=0,
                 priority=0,
                 direction=None,
                 can_push=True,
                 phase=1,
                 moved_object=to_dummy_movable(0, 0, Direction.NORTH))
