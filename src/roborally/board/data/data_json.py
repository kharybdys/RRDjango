import json
from dataclasses import asdict, dataclass, field
from typing import Optional

from roborally.board.data.loader import BoardLoader, BoardDataProvider, ScenarioDataProvider
from roborally.game.direction import Direction, to_optional_direction
from roborally.models import ElementTypes


@dataclass
class BoardElementData:
    x_coordinate: int
    y_coordinate: int
    element_type: ElementTypes
    direction: Optional[Direction] = None


@dataclass
class ScenarioFlagData:
    x_coordinate: int
    y_coordinate: int
    order_number: int


@dataclass
class ScenarioBoardData:
    turns: int
    offset_x: int
    offset_y: int
    board_data: list[dict] = field(default_factory=list)


class JSONBoardDataProvider(BoardDataProvider):
    def __init__(self, board_data: list[dict]):
        board_elements = [self._to_board_element_data(element) for element in board_data]
        self.max_x = 0
        self.max_y = 0

        for board_element in board_elements:
            self.max_x = max(self.max_x, board_element.x_coordinate)
            self.max_y = max(self.max_y, board_element.y_coordinate)

        self.elements = [asdict(element) for element in board_elements if element.element_type not in [ElementTypes.WALL, ElementTypes.LASER]]
        self.walls = [asdict(element) for element in board_elements if element.element_type == ElementTypes.WALL]
        self.lasers = [asdict(element) for element in board_elements if element.element_type == ElementTypes.LASER]

    @staticmethod
    def _to_board_element_data(element_dict: dict):
        direction = to_optional_direction(element_dict.get("direction", None))
        return BoardElementData(**dict(element_dict, direction=direction))


class JSONScenarioDataProvider(ScenarioDataProvider):
    def __init__(self, scenario_data: str):
        resource_dict = json.loads(s=scenario_data)
        self.flags = [ScenarioFlagData(**flag) for flag in resource_dict["flags"]]
        self.boards = [ScenarioBoardData(**board) for board in resource_dict["boards"]]

    def get_loader_for_boards(self):
        return [BoardLoader(board.turns, board.offset_x, board.offset_y, JSONBoardDataProvider(board.board_data)) for board in self.boards]
