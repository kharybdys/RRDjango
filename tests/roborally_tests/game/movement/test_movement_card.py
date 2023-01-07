import json
from functools import partial
from importlib.resources import files

import pytest

from roborally.board.scenario import Scenario
from roborally.game.movable import Movable
from roborally_tests.game.data import to_movable_movement_and_expectation
from roborally_tests.game.events import ExpectedEvent, EventChecker
from roborally_tests.mocks import Expectation


def load_test_data():
    with files(__package__).joinpath("scenario_card_movement_tests.json").open("r") as f:
        test_dicts = json.loads(f.read())
        for test_dict in test_dicts:
            event_checker = EventChecker()
            movables, _, expectations = zip(*map(partial(to_movable_movement_and_expectation, event_checker), test_dict["movables"]))
            expectations = filter(None, expectations)
            if test_dict.get("expected_events", None):
                for event_dict in test_dict["expected_events"]:
                    event_checker.add_expected_event(ExpectedEvent(**event_dict))
            yield pytest.param(movables,
                               expectations,
                               event_checker,
                               id=test_dict["test_id"])


@pytest.mark.parametrize('movables, expectations, event_checker', load_test_data())
def test_scenario_process_robot_movement(get_test_scenario: Scenario,
                                         movables: list[Movable],
                                         expectations: list[Expectation],
                                         event_checker: EventChecker):
    scenario = get_test_scenario

    for movable in movables:
        scenario.add_movable(movable)

    scenario.process_robot_movements(1, 1)

    for expectation in expectations:
        expectation.verify()

    assert not event_checker.has_events_remaining()
