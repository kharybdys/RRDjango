from dataclasses import dataclass, field

from roborally.game.events import EventType


@dataclass
class ExpectedEvent:
    event_type: str
    phase: int
    actor_type: str = None
    actor_order_nr: int = None
    victim_type: str = None
    victim_order_nr: int = None
    extra: dict = field(default_factory=dict)


class EventChecker:
    def __init__(self):
        self.expected_events: list[ExpectedEvent] = []

    def add_expected_event(self, expected_event: ExpectedEvent):
        self.expected_events.append(expected_event)

    def log_event(self, phase: int, event_type: EventType, registrar_type: str, registrar_order_nr: int, other_type: str, other_order_nr: int, **kwargs):
        expected_event = ExpectedEvent(event_type.value, phase, registrar_type, registrar_order_nr, other_type, other_order_nr, kwargs)
        # Throws ValueError if not found which is what we want for the test
        self.expected_events.remove(expected_event)

    def has_events_remaining(self) -> bool:
        return len(self.expected_events) > 0
