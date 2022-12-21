from contextlib import contextmanager
from typing import Any

import pytest

from roborally_tests.game.movement.data import get_movement_event_exception_class
from roborally.game.direction import to_optional_direction
from roborally_tests.mocks import CoordinatesWithDirection


def to_expectation(expectation_dict: dict) -> (CoordinatesWithDirection, Any):
    direction = to_optional_direction(expectation_dict.get("facing_direction", None))
    expected_exception = expectation_dict.pop("expected_exception", None)
    if expected_exception:
        context_manager =  pytest.raises(get_movement_event_exception_class(expected_exception))
    else:
        context_manager = does_not_raise()
    return CoordinatesWithDirection(**dict(expectation_dict, facing_direction=direction)), context_manager


@contextmanager
def does_not_raise():
    yield
