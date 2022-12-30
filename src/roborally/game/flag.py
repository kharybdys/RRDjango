from roborally.board.basic import Point
from roborally.game.movable import Movable
from roborally.game.direction import Direction
from roborally.models import ScenarioFlag


class Flag(Movable):
    PUSHABLE = False
    PUSHES = False
    HAS_DIRECTION = False

    # TODO: Should also allow Flag as a Model.
    # Possibly when coming from a scenario the ScenarioFlag should be transformed into a flag?
    def __init__(self, flag: ScenarioFlag):
        super().__init__()
        self.model = flag

    def save(self):
        self.model.save()

    def to_data(self):
        return {self.KEY_SYMBOL: str(self.model.order_number)}

    @property
    def coordinates(self):
        return Point(self.model.x_coordinate, self.model.y_coordinate)

    def update_coordinates_and_direction(self, new_coordinates: Point, new_direction: Direction):
        self.model.x_coordinate = new_coordinates.x
        self.model.y_coordinate = new_coordinates.y

    @property
    def order_number(self):
        return self.model.order_number
