import json
from importlib.resources import files

import pytest

from roborally.board.scenario import Scenario
from roborally.game.movable import Movable
from roborally_tests.game.data import to_movable_movement_and_expectation
from roborally_tests.game.events import TestEventHandler, ExpectedEvent
from roborally_tests.mocks import Expectation


def load_test_data():
    with files(__package__).joinpath("scenario_card_movement_tests.json").open("r") as f:
        test_dicts = json.loads(f.read())
        for test_dict in test_dicts:
            movables, _, expectations = zip(*map(to_movable_movement_and_expectation, test_dict["movables"]))
            event_handler = TestEventHandler()
            expectations = filter(None, expectations)
            if test_dict.get("expected_events", None):
                for event_dict in test_dict["expected_events"]:
                    event_handler.add_expected_event(ExpectedEvent(**event_dict))
            yield pytest.param(movables,
                               expectations,
                               event_handler,
                               id=test_dict["test_id"])


@pytest.mark.parametrize('movables, expectations, event_handler', load_test_data())
def test_scenario_process_robot_movement(get_test_scenario: Scenario,
                                         movables: list[Movable],
                                         expectations: list[Expectation],
                                         event_handler: TestEventHandler):
    scenario = get_test_scenario
    scenario.event_handler = event_handler

    for movable in movables:
        scenario.add_movable(movable)

    scenario.process_robot_movements(1, 1)

    for expectation in expectations:
        expectation.verify()

    assert not event_handler.has_events_remaining()
