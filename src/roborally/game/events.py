from abc import abstractmethod
from enum import Enum

from roborally.game.movable import Movable


class EventType(Enum):
    BOT_PUSHES = 'BOT_PUSHES'
    CONVEYORBELT_STALL = 'CONVEYORBELT_STALL'
    BOT_SHOOTS = 'BOT_SHOOTS'
    BOARD_SHOOTS = 'BOARD_SHOOTS'
    BOT_DIES_DAMAGE = 'BOT_DIES_DAMAGE'
    BOT_DIES_HOLE = 'BOT_DIES_HOLE'
    ARCHIVE_MARKER_MOVED = 'ARCHIVE_MARKER_MOVED'
    POWER_DOWN = 'POWER_DOWN'
    BOT_HITS_WALL = 'BOT_HITS_WALL'
    BOT_HITS_UNMOVABLE_BOT = 'BOT_HITS_UNMOVABLE_BOT'

    @classmethod
    def get_choices(cls):
        return [(key.value, key.name) for key in cls]


class PublishMixin:
    @abstractmethod
    def log_event(self, phase: int, event_type: EventType, actor: Movable = None, victim: Movable = None, **kwargs):
        pass


class EventHandler:
    # TODO: At the end check if this can again be the Game game instead of the GameModel
    def __init__(self, publisher: PublishMixin):
        self.publisher = publisher
        self.phase = 1

    def _log_event(self, event_type: EventType, actor: Movable = None, victim: Movable = None, **kwargs):
        self.publisher.log_event(self.phase, event_type, actor, victim, **kwargs)

    def log_movable_collides_against_wall(self, movable: Movable):
        self._log_event(event_type=EventType.BOT_HITS_WALL, actor=movable)

    def log_movable_collides_against_movable(self, actor: Movable, victim: Movable):
        self._log_event(event_type=EventType.BOT_HITS_UNMOVABLE_BOT, actor=actor, victim=victim)

    def log_movable_killed_hole(self, movable: Movable):
        self._log_event(event_type=EventType.BOT_DIES_HOLE, actor=movable)

    def log_board_movement_impossible(self, movable: Movable):
        self._log_event(event_type=EventType.CONVEYORBELT_STALL, actor=movable)


class DummyEventHandler(EventHandler):
    def __init__(self):
        super().__init__(None)

    def _log_event(self, event_type: EventType, actor: Movable = None, victim: Movable = None, **kwargs):
        print(f"{event_type=}, {actor=}, {victim=}")
