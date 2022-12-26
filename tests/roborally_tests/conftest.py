import pytest

from roborally.board.scenario import Scenario
from roborally_tests.board.data import get_test_scenario_data_provider
from roborally_tests.game.events import TestEventHandler


@pytest.fixture
def get_test_scenario(load_flags: bool = False) -> Scenario:
    scenario_data_provider = get_test_scenario_data_provider()
    return Scenario(scenario_data_provider=scenario_data_provider, event_handler=TestEventHandler(),
                    load_flags=load_flags)
