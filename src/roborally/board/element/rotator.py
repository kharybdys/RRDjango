from abc import ABCMeta

from roborally.board.element.basic import BasicElement
from roborally.game import movement
from roborally.game.basic import BasicMovableElement


class Rotator(BasicElement, metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self.turns = 0

    def board_movements(self, phase: int, movable: BasicMovableElement):
        return [movement.Movement(direction=None,
                                  steps=0,
                                  turns=self.turns,
                                  priority=0,
                                  movement_type=movement.TYPE_ROTATOR,
                                  moved_object=movable)]


class ClockwiseRotator(Rotator):
    def __init__(self):
        super().__init__()
        self.turns = 1


class CounterClockwiseRotator(Rotator):
    def __init__(self):
        super().__init__()
        self.turns = -1
