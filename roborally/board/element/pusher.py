from roborally.board.element.basic import BasicElement, KEY_ELEMENT_TYPE
from roborally.models import ElementTypes
from roborally.game import movement


class Pusher(BasicElement):

    def __init__(self, direction):
        super().__init__()
        self.direction = direction
        self.phases = []
        self.type = None  # Not to be used so no type

    def to_data(self):
        return {KEY_ELEMENT_TYPE: self.type,
                'direction': self.direction,
                'symbol': ' '.join(map(str, self.phases))}

    def board_movements(self, phase):
        if phase in self.phases:
            return [movement.Movement(direction=self.direction,
                                      steps=1,
                                      turns=0,
                                      priority=0,
                                      movement_type=movement.TYPE_PUSHER)]
        else:
            return []


class Pusher135(Pusher):
    def __init__(self, direction):
        super().__init__(direction)
        self.phases = [1, 3, 5]
        self.type = ElementTypes.PUSHER_135


class Pusher24(Pusher):
    def __init__(self, direction):
        super().__init__(direction)
        self.phases = [2, 4]
        self.type = ElementTypes.PUSHER_24
