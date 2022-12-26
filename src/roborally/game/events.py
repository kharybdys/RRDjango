from roborally.game.basic import Movable
from roborally.game.bot import Bot
from roborally.models import EventType, Game


class EventHandler:
    # TODO: At the end check if this can again be the Game game instead of the GameModel
    def __init__(self, game: Game):
        self.game = game
        self.phase = 1

    def _log_event(self, event_type: EventType, actor: Bot = None, victim: Bot = None, **kwargs):
        self.game.log_event(self.phase, event_type, actor, victim, **kwargs)

    def log_movable_collides_against_wall(self, movable: Movable):
        if isinstance(movable, Bot):
            self._log_event(event_type=EventType.BOT_HITS_WALL, actor=movable)
        else:
            # Flags colliding is not interesting?
            pass

    def log_movable_collides_against_movable(self, actor: Movable, victim: Movable):
        if isinstance(actor, Bot) and isinstance(victim, Bot):
            self._log_event(event_type=EventType.BOT_HITS_UNMOVABLE_BOT, actor=actor, victim=victim)
        else:
            # Flags colliding is not interesting?
            pass

    def log_movable_killed_hole(self, movable: Movable):
        if isinstance(movable, Bot):
            self._log_event(event_type=EventType.BOT_DIES_HOLE, actor=movable)
        else:
            # TODO: Support logging events on flags
            print("Flag died, TODO")

    def log_board_movement_impossible(self, movable: Movable):
        if isinstance(movable, Bot):
            self._log_event(event_type=EventType.CONVEYORBELT_STALL, actor=movable)
        else:
            # TODO: Support logging events on flags
            print("Flag cannot move due to blocking items, TODO")
