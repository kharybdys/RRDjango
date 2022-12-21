# Responsible for loading the base testdata, ie a scenario
from importlib.resources import files

from roborally.board.data.data_django import ScenarioDataProvider
from roborally.board.data.data_json import JSONScenarioDataProvider


def get_test_scenario_data_provider() -> ScenarioDataProvider:
    with files(__package__).joinpath("test_scenario.json").open('r') as f:
        return JSONScenarioDataProvider(f.read())
