from abc import ABCMeta

from roborally.game.basic import BasicMovableElement
from roborally.game.bot import Bot
from roborally.game.events import EventHandler
from roborally.models import EventType


class HappenedMixin:
    happened = False


class TestEventHandler(EventHandler, HappenedMixin, metaclass=ABCMeta):
    def __init__(self):
        super().__init__(None)

    def _log_event(self, event_type: EventType, actor: Bot = None, victim: Bot = None, **kwargs):
        assert False, "Should not happen"


class BaseTestEventHandler(TestEventHandler):
    happened = True


class MovableDiedEventHandler(TestEventHandler):
    def log_movable_killed_hole(self, movable: BasicMovableElement):
        self.happened = True


class MovableCollidedWallEventHandler(TestEventHandler):
    def log_movable_collides_against_wall(self, movable: BasicMovableElement):
        self.happened = True


def get_test_event_handler_for(event_name: str):
    match event_name:
        case "MOVABLE_DIED":
            return MovableDiedEventHandler()
        case "MOVABLE_COLLIDED_WALL":
            return MovableCollidedWallEventHandler()
        case _:
            return BaseTestEventHandler()
