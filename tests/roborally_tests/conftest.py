import pytest

from roborally.board.scenario import Scenario
from roborally_tests.board.data import get_test_scenario_data_provider


@pytest.fixture
def get_test_scenario(load_flags: bool = False) -> Scenario:
    scenario_data_provider = get_test_scenario_data_provider()
    return Scenario(scenario_data_provider=scenario_data_provider, load_flags=load_flags)
