from roborally.board.basic import Point
from roborally.game.basic import BasicMovableElement, KEY_SYMBOL
from roborally.models import Bot as BotModel


class Bot(BasicMovableElement):
    INITIAL_HEALTH = 10

    def __init__(self, bot: BotModel):
        super().__init__()
        self.model = bot

    def save(self):
        if self.model:
            self.model.save()

    def to_data(self):
        return {KEY_SYMBOL: str(self.model.order_number)}

    @property
    def coordinates(self):
        return Point(self.model.x_coordinate, self.model.y_coordinate)

    @property
    def damage(self):
        return self.model.damage
