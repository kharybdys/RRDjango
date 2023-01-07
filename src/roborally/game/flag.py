from roborally.board.basic import Point
from roborally.game.card import CardDefinition
from roborally.game.events import EventType
from roborally.game.movable import Movable
from roborally.game.direction import Direction
from roborally.models import Flag as FlagModel


class Flag(Movable):
    PUSHABLE = False
    PUSHES = False
    HAS_DIRECTION = False

    # TODO: Should also allow Flag as a Model.
    # Possibly when coming from a scenario the ScenarioFlag should be transformed into a flag?
    def __init__(self, flag: FlagModel):
        super().__init__()
        self.model = flag

    def save(self):
        self.model.save()

    def to_data(self):
        return {self.KEY_TYPE: self.__class__.__name__, self.KEY_SYMBOL: str(self.model.order_number), **self.coordinates.to_data()}

    @property
    def coordinates(self):
        return Point(self.model.x_coordinate, self.model.y_coordinate)

    @property
    def archive_coordinates(self):
        return Point(self.model.archive_x_coordinate, self.model.archive_y_coordinate)

    def update_coordinates_and_direction(self, new_coordinates: Point, new_direction: Direction):
        self.model.x_coordinate = new_coordinates.x
        self.model.y_coordinate = new_coordinates.y

    @property
    def order_number(self):
        return self.model.order_number

    def get_cards_for(self, round: int, phase: int) -> list[CardDefinition]:
        return []

    def _log_event(self, phase: int, event_type: EventType, other: Movable = None, **kwargs):
        pass

    @property
    def damage(self) -> int:
        return 0

    def take_damage(self, damage: int):
        pass

