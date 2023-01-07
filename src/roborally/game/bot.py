from roborally.board.basic import Point
from roborally.game.card import CardDefinition
from roborally.game.events import EventType
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
        return {self.KEY_TYPE: self.__class__.__name__, self.KEY_SYMBOL: str(self.model.order_number), **self.coordinates.to_data()}

    @property
    def coordinates(self):
        return Point(self.model.x_coordinate, self.model.y_coordinate)

    @property
    def archive_coordinates(self):
        return Point(self.model.archive_x_coordinate, self.model.archive_y_coordinate)

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

    def cleanup_killed_at_model(self):
        self.model.damage = 2

    def get_cards_for(self, round: int, phase: int) -> list[CardDefinition]:
        return self.model.get_cards_for(round=round, phase=phase)

    def take_damage(self, damage: int):
        if self.model.damage + damage >= self.INITIAL_HEALTH:
            pass

    def _log_event(self, phase: int, event_type: EventType, other: Movable = None, **kwargs):
        other_model = None
        if other and isinstance(other, Bot):
            other_model = other.model
        self.model.log_event(phase, event_type, other_model, **kwargs)
