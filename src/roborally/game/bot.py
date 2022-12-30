from roborally.board.basic import Point
from roborally.game.movable import Movable
from roborally.game.direction import Direction
from roborally.models import Bot as BotModel


class Bot(Movable):
    INITIAL_HEALTH = 10

    def __init__(self, bot: BotModel):
        super().__init__()
        self.model = bot

    def save(self):
        self.model.save()

    def to_data(self):
        return {self.KEY_SYMBOL: str(self.model.order_number)}

    @property
    def coordinates(self):
        return Point(self.model.x_coordinate, self.model.y_coordinate)

    @property
    def facing_direction(self):
        return self.model.facing_direction

    def update_coordinates_and_direction(self, new_coordinates: Point, new_direction: Direction):
        self.model.x_coordinate = new_coordinates.x
        self.model.y_coordinate = new_coordinates.y
        self.model.facing_direction = new_direction

    @property
    def order_number(self):
        return self.model.order_number

    @property
    def damage(self):
        return self.model.damage
