from abc import ABCMeta

import roborally.game.direction
from roborally.board.element.basic import BasicElement
from roborally.game import movement
from roborally.game.basic import BasicMovableElement
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

    def board_movements(self, phase: int, movable: BasicMovableElement) -> list[movement.Movement]:
        return self._basic_board_movements(movable)

    # Implements the movement this exact boardElement causes, without taking into account
    # that dual speed conveyor belts may have us end up on another conveyor belt that will still move

    # Implements:
    # 1) Basic movement of the conveyor
    # 2) Extra turn action because of the turn in the conveyor we just took

    def _basic_board_movements(self, movable: BasicMovableElement) -> list[movement.Movement]:
        move = movement.Movement(direction=self.end_direction,
                                 steps=1,
                                 turns=0,
                                 priority=200,
                                 movement_type=movement.TYPE_SINGLE_CONVEYOR,
                                 moved_object=movable)
        neighbour = self.get_neighbour(self.end_direction)
        if isinstance(neighbour, Conveyor):
            if neighbour.end_direction != self.end_direction:
                turn = movement.Movement(direction=None,
                                         steps=0,
                                         turns=self.end_direction.turns_to(neighbour.end_direction),
                                         priority=100,
                                         movement_type=movement.TYPE_SINGLE_CONVEYOR,
                                         moved_object=movable)
                return [move, turn]
            else:
                return [move]
        else:
            return [move]


class SingleSpeedConveyor(Conveyor):
    pass


class DualSpeedConveyor(Conveyor):

    def board_movements(self, phase: int, movable: BasicMovableElement) -> list[movement.Movement]:
        """
        Make sure to handle the scenarios of two steps on a dual conveyor, but also a dual conveyor dropping you
        on a single conveyor (which will still move you)
        """
        moves = [self._increase_priority_and_mark_as_dual(move) for move in self._basic_board_movements(movable)]
        neighbour = self.get_neighbour(self.end_direction)
        if isinstance(neighbour, Conveyor):
            moves.extend(neighbour._basic_board_movements(movable))
        return moves

    @staticmethod
    def _increase_priority_and_mark_as_dual(move: movement.Movement) -> movement.Movement:
        new_move = movement.Movement(direction=move.direction,
                                     steps=move.steps,
                                     turns=move.turns,
                                     priority=move.priority * 3,
                                     movement_type=movement.TYPE_DUAL_CONVEYOR,
                                     moved_object=move.moved_object)
        return new_move


