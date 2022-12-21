from typing import Type

from roborally.game import events
from roborally.game.basic import BasicMovableElement
from roborally.game.bot import Bot
from roborally_tests.mocks import CoordinatesWithDirection


def get_movement_event_exception_class(class_name) -> Type[events.EventException]:
    return getattr(events, class_name)


def verify(movable: BasicMovableElement, expectation: CoordinatesWithDirection):
    assert movable.coordinates.x == expectation.x_coordinate
    assert movable.coordinates.y == expectation.y_coordinate
    if isinstance(movable, Bot):
        assert movable.facing_direction == expectation.facing_direction
