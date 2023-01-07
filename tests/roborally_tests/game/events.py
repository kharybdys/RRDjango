from dataclasses import dataclass, field

from roborally.game.events import EventType
from roborally.game.movable import Movable


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
    def create_one(event_type: EventType, phase: int, registrar: "MovableModelMock", other: "MovableModelMock", **kwargs):
        return ExpectedEvent(event_type=event_type.value,
                             phase=phase,
                             actor_type=registrar.type,
                             actor_order_nr=registrar.order_number,
                             victim_type=registrar.type if other else None,
                             victim_order_nr=other.order_number if other else None,
                             extra=kwargs)
        pass


# TODO: Another circular import problem due to type checking
class EventChecker:
    def __init__(self):
        self.expected_events: list[ExpectedEvent] = []

    def add_expected_event(self, expected_event: ExpectedEvent):
        self.expected_events.append(expected_event)

    def log_event(self, phase: int, event_type: EventType, registrar: "MovableModelMock", other: Movable = None, **kwargs):
        expected_event = ExpectedEvent.create_one(event_type, phase, registrar, other.model if other else None, **kwargs)
        # Throws ValueError if not found which is what we want for the test
        self.expected_events.remove(expected_event)

    def has_events_remaining(self) -> bool:
        return len(self.expected_events) > 0
