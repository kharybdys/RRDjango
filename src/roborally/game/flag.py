from roborally.board.basic import Point
from roborally.game.basic import BasicMovableElement, KEY_SYMBOL
from roborally.models import ScenarioFlag

TYPE_FLAG = 'FLAG'


class Flag(BasicMovableElement):

    def __init__(self, flag: ScenarioFlag):
        super().__init__()
        self.model = flag

    def save(self):
        if self.model:
            self.model.save()

    def to_data(self):
        return {KEY_SYMBOL: str(self.model.order_number)}

    @property
    def coordinates(self):
        return Point(self.model.x_coordinate, self.model.y_coordinate)
