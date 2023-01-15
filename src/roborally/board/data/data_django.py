from roborally.board.data.loader import BoardLoader, BoardDataProvider, ScenarioDataProvider, ElementTypes
from roborally.models.scenario import BoardElement, ScenarioFlag, ScenarioBoard


class DjangoBoardDataProvider(BoardDataProvider):
    def __init__(self, board_name: str):
        board = BoardElement.objects.filter(name=board_name)

        self.max_x = 0
        self.max_y = 0

        for board_element in board:
            self.max_x = max(self.max_x, board_element.x_coordinate)
            self.max_y = max(self.max_y, board_element.y_coordinate)

        self.elements = map(BoardElement.to_dict,
                            board.exclude(element_type__in=[ElementTypes.WALL, ElementTypes.LASER]))
        self.walls = map(BoardElement.to_dict, board.filter(element_type=ElementTypes.WALL))
        self.lasers = map(BoardElement.to_dict, board.filter(element_type=ElementTypes.LASER))


class DjangoScenarioDataProvider(ScenarioDataProvider):
    def __init__(self, scenario_name: str):
        self.flags = ScenarioFlag.objects.filter(name=scenario_name)
        self.boards = ScenarioBoard.objects.filter(name=scenario_name)

    def get_loader_for_boards(self):
        return [BoardLoader(board.turns, board.offset_x, board.offset_y, DjangoBoardDataProvider(board.board_name)) for board in self.boards]
