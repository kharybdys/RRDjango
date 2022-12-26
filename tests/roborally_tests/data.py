from roborally.game.direction import to_optional_direction
from roborally_tests.game.events import get_test_event_handler_for
from roborally_tests.mocks import Expectation


def to_expectation(expectation_dict: dict) -> Expectation:
    direction = to_optional_direction(expectation_dict.get("facing_direction", None))
    expected_event = expectation_dict.pop("expected_event", None)
    event_handler = get_test_event_handler_for(expected_event)
    return Expectation(**dict(expectation_dict, facing_direction=direction, event_handler=event_handler))
