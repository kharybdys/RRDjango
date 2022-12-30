from abc import ABCMeta

from roborally.board.element.basic import BasicElement
from roborally.game import movement
from roborally.game.movable import Movable
from roborally.game.direction import Direction


class Pusher(BasicElement, metaclass=ABCMeta):

    def __init__(self, direction: Direction):
        super().__init__()
        self.direction = direction
        self.phases: list[int] = []

    def to_data(self) -> dict:
        element_data = super().to_data()
        element_data[self.KEY_DIRECTION] = self.direction.value
        element_data[self.KEY_SYMBOL] = ' '.join(map(str, self.phases))
        return element_data

    def board_movements(self, phase: int, movable: Movable) -> movement.Movement | None:
        if phase in self.phases:
            return movement.Movement(direction=self.direction,
                                     steps=1,
                                     turns=0,
                                     priority=0,
                                     can_push=False,
                                     moved_object=movable)
        else:
            return None


class Pusher135(Pusher):
    def __init__(self, direction: Direction):
        super().__init__(direction)
        self.phases = [1, 3, 5]


class Pusher24(Pusher):
    def __init__(self, direction: Direction):
        super().__init__(direction)
        self.phases = [2, 4]
