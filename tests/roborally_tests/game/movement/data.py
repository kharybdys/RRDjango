from roborally.game.basic import BasicMovableElement
from roborally.game.bot import Bot
from roborally_tests.mocks import Expectation


def verify(movable: BasicMovableElement, expectation: Expectation):
    assert movable.coordinates.x == expectation.x_coordinate
    assert movable.coordinates.y == expectation.y_coordinate
    if isinstance(movable, Bot) and expectation.facing_direction:
        assert movable.facing_direction == expectation.facing_direction
    if expectation.event_handler:
        assert expectation.event_handler.happened
