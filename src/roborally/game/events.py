from abc import abstractmethod
from enum import Enum


class EventType(Enum):
    BOT_PUSHES = 'BOT_PUSHES'
    CONVEYORBELT_STALL = 'CONVEYORBELT_STALL'
    BOT_SHOOTS = 'BOT_SHOOTS'
    BOARD_SHOOTS = 'BOARD_SHOOTS'
    BOT_DIES_DAMAGE = 'BOT_DIES_DAMAGE'
    MOVABLE_DIES_HOLE = 'BOT_DIES_HOLE'
    ARCHIVE_MARKER_MOVED = 'ARCHIVE_MARKER_MOVED'
    POWER_DOWN = 'POWER_DOWN'
    MOVABLE_HITS_WALL = 'BOT_HITS_WALL'
    BOT_HITS_UNMOVABLE_BOT = 'BOT_HITS_UNMOVABLE_BOT'

    @classmethod
    def get_choices(cls):
        return [(key.value, key.name) for key in cls]


# TODO: See if this circular import can be solved
class PublishMixin:
    @abstractmethod
    def _log_event(self, phase: int, event_type: EventType, other: "Movable" = None, **kwargs):
        pass

    def log_collides_against_wall(self, phase: int):
        self._log_event(phase=phase, event_type=EventType.MOVABLE_HITS_WALL)

    def log_collides_against_movable(self, phase: int, victim: "Movable"):
        self._log_event(phase=phase, event_type=EventType.BOT_HITS_UNMOVABLE_BOT, other=victim)

    def log_killed_by_hole(self, phase: int):
        self._log_event(phase=phase, event_type=EventType.MOVABLE_DIES_HOLE)

    def log_killed_by_damage(self, phase: int):
        self._log_event(phase=phase, event_type=EventType.BOT_DIES_DAMAGE)

    def log_board_movement_impossible(self, phase: int):
        self._log_event(phase=phase, event_type=EventType.CONVEYORBELT_STALL)
