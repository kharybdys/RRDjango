from roborally.board.element.basic import BasicElement, KEY_ELEMENT_TYPE
from roborally.models import ElementTypes
from roborally.game import movement


def _upgrade(move):
    new_move = movement.Movement(direction=move.direction,
                                 steps=move.steps,
                                 turns=move.turns,
                                 priority=move.priority * 3,
                                 movement_type=movement.TYPE_DUAL_CONVEYOR)
    return new_move


class Conveyor(BasicElement):

    def __init__(self, end_direction):
        super().__init__()
        self.end_direction = end_direction
        self.starting_directions = []
        self.type = None  # Not to be used so no type

    def set_neighbour(self, direction, element):
        super().set_neighbour(direction, element)
        if self.end_direction != direction and element.type == self.type:
            neighbour_end_direction = element.end_direction;
            if movement.get_to_direction(direction, 2) == neighbour_end_direction:
                self.starting_directions.append(direction)

    def neighbours_completed(self):
        if not self.starting_directions:
            self.starting_directions.append(movement.get_to_direction(self.end_direction, 2))

    def to_data(self):
        return {KEY_ELEMENT_TYPE: self.type,
                'starting_directions': self.starting_directions,
                'end_direction': self.end_direction}

    def board_movements(self, phase):
        return self.basic_board_movements()

    # Implements the movement this exact boardElement causes, without taking into account
    # that dual speed conveyor belts may have us end up on another conveyor belt that will still move

    # Implements:
    # 1) Basic movement of the conveyor
    # 2) Extra turn action because of the turn in the conveyor we just took

    def basic_board_movements(self):
        move = movement.Movement(direction=self.end_direction,
                                 steps=1,
                                 turns=0,
                                 priority=200,
                                 movement_type=movement.TYPE_SINGLE_CONVEYOR)
        neighbour = self.get_neighbour(self.end_direction)
        if neighbour.type in [ElementTypes.SINGLE_CONVEYOR, ElementTypes.DUAL_CONVEYOR]:
            if neighbour.end_direction != self.end_direction:
                turn = movement.Movement(direction=None,
                                         steps=0,
                                         turns=movement.get_turns(self.end_direction, neighbour.end_direction),
                                         priority=100,
                                         movement_type=movement.TYPE_SINGLE_CONVEYOR)
                return [move, turn]
            else:
                return [move]
        else:
            return [move]


class SingleSpeedConveyor(Conveyor):
    def __init__(self, end_direction):
        super().__init__(end_direction)
        self.type = ElementTypes.SINGLE_CONVEYOR


class DualSpeedConveyor(Conveyor):
    def __init__(self, end_direction):
        super().__init__(end_direction)
        self.type = ElementTypes.DUAL_CONVEYOR

    def board_movements(self, phase):
        moves = [_upgrade(move) for move in self.basic_board_movements()]
        neighbour = self.get_neighbour(self.end_direction)
        if neighbour.type in [ElementTypes.SINGLE_CONVEYOR, ElementTypes.DUAL_CONVEYOR]:
            moves.append(neighbour.basic_board_movements())
        return moves
