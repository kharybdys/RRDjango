from roborally.game.basic import Movable
from roborally.game.bot import Bot
from roborally.models import EventType, Game


class EventHandler:
    # TODO: At the end check if this can again be the Game game instead of the GameModel
    def __init__(self, game: Game):
        self.game = game
        self.phase = 1

    def _log_event(self, event_type: EventType, actor: Movable = None, victim: Movable = None, **kwargs):
        if (not actor or isinstance(actor, Bot)) and (not victim or isinstance(victim, Bot)):
            self.game.log_event(self.phase, event_type, actor, victim, **kwargs)
        else:
            # TODO: Support logging events on flags
            print(f"{event_type=}, {actor=}, {victim=}")

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
