from roborally.board.element.basic import BasicElement
from roborally.models import ElementTypes
from roborally.game import movement


class Rotator(BasicElement):

    def __init__(self):
        super().__init__()
        self.turns = 0
        self.type = None  # Not to be used so no type

    def board_movements(self, phase):
        return [movement.Movement(direction=None,
                                  steps=0,
                                  turns=self.turns,
                                  priority=0,
                                  movement_type=movement.TYPE_ROTATOR)]


class ClockwiseRotator(Rotator):
    def __init__(self):
        super().__init__()
        self.type = ElementTypes.ROTATOR_CLOCKWISE
        self.turns = 1


class CounterClockwiseRotator(Rotator):
    def __init__(self):
        super().__init__()
        self.type = ElementTypes.ROTATOR_COUNTERCLOCKWISE
        self.turns = -1
