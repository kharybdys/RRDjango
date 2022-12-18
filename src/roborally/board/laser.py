from roborally.game.direction import Direction
from roborally.utils.codec import SerializationMixin


class LaserMixin(SerializationMixin):
    def __init__(self, shooting_direction: Direction, hits: int = 1):
        self.shooting_direction = shooting_direction
        self.hits = hits

    def to_data(self):
        return {self.KEY_DIRECTION: self.shooting_direction.value,
                'hits': self.hits}


class Laser(LaserMixin):
    pass

