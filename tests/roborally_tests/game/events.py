from dataclasses import dataclass, field

from roborally.game.basic import Movable
from roborally.game.bot import Bot
from roborally.game.events import EventHandler
from roborally.models import EventType


@dataclass
class ExpectedEvent:
    event_type: str
    phase: int
    actor_type: str = None
    actor_order_nr: int = None
    victim_type: str = None
    victim_order_nr: int = None
    extra: dict = field(default_factory=dict)

    @staticmethod
    def create_one(event_type: EventType, phase: int, actor: Movable | None, victim: Movable | None, **kwargs):
        return ExpectedEvent(event_type=str(event_type),
                             phase=phase,
                             actor_type=actor.__class__.__name__ if actor else None,
                             actor_order_nr=actor.order_number if actor else None,
                             victim_type=actor.__class__.__name__ if victim else None,
                             victim_order_nr=victim.order_number if victim else None,
                             extra=kwargs)
        pass


class TestEventHandler(EventHandler):
    def __init__(self):
        super().__init__(None)
        self.expected_events: list[ExpectedEvent] = []

    def add_expected_event(self, expected_event: ExpectedEvent):
        self.expected_events.append(expected_event)

    def _log_event(self, event_type: EventType, actor: Bot = None, victim: Bot = None, **kwargs):
        expected_event = ExpectedEvent.create_one(event_type, self.phase, actor, victim, **kwargs)
        # Throws ValueError if not found which is what we want for the test
        self.expected_events.remove(expected_event)

    def has_events_remaining(self) -> bool:
        return len(self.expected_events) > 0
