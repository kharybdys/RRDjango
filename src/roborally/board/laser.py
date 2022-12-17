from roborally.models import Direction


class LaserMixin:
    def __init__(self, shooting_direction: Direction, hits: int = 1):
        self.shooting_direction = shooting_direction
        self.hits = hits

    def to_data(self):
        return {'direction': self.shooting_direction,
                'hits': self.hits}


class Laser(LaserMixin):
    pass

