from abc import ABCMeta

import roborally.game.direction
from roborally.board.element.basic import BasicElement
from roborally.game import movement
from roborally.game.movable import Movable
from roborally.game.direction import Direction


class Conveyor(BasicElement, metaclass=ABCMeta):

    def __init__(self, end_direction: Direction):
        super().__init__()
        self.end_direction = end_direction
        self.starting_directions: list[Direction] = []

    def set_neighbour(self, direction: Direction, element: BasicElement):
        super().set_neighbour(direction, element)
        if self.end_direction != direction and isinstance(element, self.__class__):
            neighbour_end_direction = element.end_direction
            if roborally.game.direction.get_to_direction(direction, 2) == neighbour_end_direction:
                self.starting_directions.append(direction)

    def neighbours_completed(self):
        if not self.starting_directions:
            self.starting_directions.append(roborally.game.direction.get_to_direction(self.end_direction, 2))

    def to_data(self) -> dict:
        element_data = super().to_data()
        element_data['starting_directions'] = [direction.value for direction in self.starting_directions]
        element_data['end_direction'] = self.end_direction.value
        return element_data

    def board_movements(self, phase: int, movable: Movable) -> movement.Movement:
        neighbour = self.get_neighbour(self.end_direction)
        return movement.Movement(direction=self.end_direction,
                                 steps=1,
                                 turns=self.end_direction.turns_to(neighbour.end_direction),
                                 priority=0,
                                 movement_type=movement.TYPE_SINGLE_CONVEYOR,
                                 moved_object=movable)


class SingleSpeedConveyor(Conveyor):
    pass


class DualSpeedConveyor(Conveyor):
    pass
