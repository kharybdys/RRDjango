import json
from importlib.resources import files

import pytest

from roborally.board.scenario import Scenario
from roborally.game.movement import Movement
from roborally.game.basic import BasicMovableElement
from roborally_tests.data import to_expectation
from roborally_tests.game.data import to_movable, to_movement
from roborally_tests.game.movement.data import verify
from roborally_tests.mocks import Expectation


# Initialization is a board and a bot/flag on a certain position in that board
# Input is one or more movement instructions for the bot/flag
# Assertion is bot/flag coordinates or error type


def load_test_data():
    with files(__package__).joinpath("scenario_process_movement_tests.json").open("r") as f:
        test_dicts = json.loads(f.read())
        for test_dict in test_dicts:
            movable = to_movable(test_dict["movable"])
            expectation = to_expectation(test_dict["expectation"])
            yield pytest.param(movable,
                               to_movement(test_dict["movement"], movable),
                               expectation,
                               id=test_dict["test_id"])


@pytest.mark.parametrize('movable, movement, expectation', load_test_data())
def test_scenario_process_movement(get_test_scenario: Scenario,
                                   movable: BasicMovableElement,
                                   movement: Movement,
                                   expectation: Expectation):
    scenario = get_test_scenario
    scenario.add_movable(movable)
    scenario.event_handler = expectation.event_handler

    scenario.process_movement(movement)
    verify(movable, expectation)
