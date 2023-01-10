from collections import defaultdict, Counter

import roborally.game.direction
from roborally.board.basic import Point
from roborally.board.element import basic
from roborally.board.element.conveyor import Conveyor, DualSpeedConveyor
from roborally.board.element.pusher import Pusher
from roborally.board.element.rotator import Rotator
from roborally.board.laser import Laser
from roborally.board.data.loader import BoardLoader, ScenarioDataProvider
from roborally.game.movable import Movable
from roborally.game.direction import Direction
from roborally.game.flag import Flag
from roborally.game.movement import Movement, MovementPossibility
from roborally.utils.codec import SerializationMixin


class Scenario(SerializationMixin):

    def __init__(self, scenario_data_provider: ScenarioDataProvider, load_flags: bool = False):
        self.y_size = 0
        self.x_size = 0
        self.elements: dict[Point, basic.BasicElement] = {}
        self.walls: dict[Point, set[Direction]] = defaultdict(set)
        self.lasers: dict[tuple[Point, Direction], Laser] = {}
        self.movables: list[Movable] = []
        for loader in scenario_data_provider.get_loader_for_boards():
            self._add_board(loader)

        self._determine_size()
        self._fill_with_void()
        if load_flags:
            for flag in scenario_data_provider.flags:
                self.add_movable(Flag(flag))
        self._fill_neighbours()
        self._validate()

    def add_movable(self, movable: Movable):
        self.movables.append(movable)

    @staticmethod
    def _generate_laser_path(start: Point, end: Point) -> list[Point]:
        """ Generates a list of coordinates going from (start_x, start_y) to (end_x, end_y), inclusive.
            Assumes either start_x and end_x are equal or start_y and end_y are equal (ie a line parallel to an axis)
        """
        x_range = list(range(min(start.x, end.x), max(start.x, end.x) + 1))  # include end
        y_range = list(range(min(start.y, end.y), max(start.y, end.y) + 1))  # include end
        x_range.extend([end.x] * (len(y_range) - len(x_range)))
        y_range.extend([end.y] * (len(x_range) - len(y_range)))
        return [Point(d[0], d[1]) for d in zip(x_range, y_range)]

    def _add_board(self, loader: BoardLoader):
        self.elements.update(loader.board_elements)
        self.walls.update(loader.walls)
        self.lasers.update(loader.lasers)

    def _determine_size(self):
        self.x_size = 0
        self.y_size = 0
        for p in self.elements.keys():
            self.x_size = max(self.x_size, p.x)
            self.y_size = max(self.y_size, p.y)

        for (p, _) in self.lasers.keys():
            self.x_size = max(self.x_size, p.x)
            self.y_size = max(self.y_size, p.y)

        for p in self.walls.keys():
            self.x_size = max(self.x_size, p.x)
            self.y_size = max(self.y_size, p.y)

        self.x_size += 1
        self.y_size += 1

    def _fill_with_void(self):
        for x in range(0, self.x_size):
            for y in range(0, self.y_size):
                if Point(x, y) not in self.elements.keys():
                    self.elements[Point(x, y)] = basic.VoidElement()

    def _fill_neighbours(self):
        void = basic.VoidElement()
        for x in range(0, self.x_size):
            for y in range(0, self.y_size):
                current_element = self.elements.get(Point(x, y))
                if current_element:
                    for direction in list(Direction):
                        neighbour = self.elements.get(Point(x, y).neighbour(direction), void)
                        current_element.set_neighbour(direction, neighbour)
                    current_element.neighbours_completed()

    def _validate(self):
        # TODO: Max 1 of each starting element
        # TODO: Every pusher must have a wall "behind" it?
        # TODO: Every laser must have a wall "behind" it
        # TODO: No duplicate coordinates for the board elements (not testable here)
        # TODO: No duplicate coordinates for flags (or later).
        # TODO: No duplicate coordinates for bots (later?)?
        pass

    def to_data(self) -> dict:
        board_data = {'factor': basic.DRAW_MAGNIFICATION_FACTOR,
                      'width': self.x_size,
                      'height': self.y_size,
                      'elements': [],
                      'walls': [],
                      'lasers': [],
                      'movables': []
                      }

        for coordinates, element in sorted(self.elements.items()):  # PyCharm can't see this is an Iterable
            element_data = element.to_data()
            element_data.update(coordinates.to_data())
            board_data['elements'].append(element_data)

        for coordinates, directions in self.walls.items():
            for direction in directions:
                wall_data = {self.KEY_DIRECTION: direction.value}
                wall_data.update(coordinates.to_data())
                board_data['walls'].append(wall_data)

        for (coordinates, direction), laser in self.lasers.items():
            laser_end = self.determine_laser_end(coordinates, direction, True)
            laser_data = laser.to_data()
            laser_data.update(coordinates.to_data())
            laser_data['laser_path'] = list(
                map(lambda p: p.to_data(), self._generate_laser_path(coordinates, laser_end)))
            board_data['lasers'].append(laser_data)

        for movable in self.movables:
            board_data['movables'].append(movable.to_data())

        return board_data

    def _pushable_at_coords(self, coordinates) -> Movable | None:
        return next(filter(lambda b: b.PUSHABLE and b.coordinates == coordinates, self.movables), None)

    def determine_laser_end(self, coordinates: Point, direction: Direction, ignore_pushables: bool) -> Point:
        # TODO: Also ignore originating bot
        if direction in self.walls[coordinates] or (not ignore_pushables and self._pushable_at_coords(coordinates)):
            return coordinates
        else:
            new_coordinates = coordinates.neighbour(direction)
            if roborally.game.direction.get_to_direction(direction, 2) in self.walls[new_coordinates]:
                return coordinates
            else:
                return self.determine_laser_end(new_coordinates, direction, ignore_pushables)

    def _process_movement(self, movement: Movement, ignore_movable_collision: bool = False) -> MovementPossibility:
        kills = False
        current_coordinates = movement.moved_object.coordinates
        if movement.direction in self.walls[current_coordinates] or movement.direction.turn(2) in self.walls[current_coordinates.neighbour(movement.direction)]:
            movement.moved_object.log_collides_against_wall(movement.phase)
            return MovementPossibility.from_movable(movement.phase, movement.moved_object)
        new_coordinates = current_coordinates
        for _ in range(0, movement.steps):
            new_coordinates = new_coordinates.neighbour(movement.direction)
        if not ignore_movable_collision and movement.moved_object.PUSHES and new_coordinates != movement.moved_object.coordinates and (pushed := self._pushable_at_coords(new_coordinates)):
            # TODO: This is too simplistic, pushing (if movement_type is robot) is missing
            movement.moved_object.log_collides_against_movable(movement.phase, pushed)
            return MovementPossibility.from_movable(movement.phase, movement.moved_object)
        if self.elements[current_coordinates].get_neighbour(movement.direction).KILLS:
            kills = True
        new_direction = movement.moved_object.facing_direction.turn(movement.turns)
        return MovementPossibility(phase=movement.phase,
                                   movable=movement.moved_object,
                                   new_coordinates=new_coordinates,
                                   new_direction=new_direction,
                                   kills=kills)

    def process_movement(self, movement: Movement):
        self._process_movement(movement).process()

    @staticmethod
    def _get_duplicated_target_coordinates(possible_movements: list[MovementPossibility]) -> Point | None:
        counted_target_coordinates = Counter([m.new_coordinates for m in possible_movements])
        duplicated_target_coordinates, duplication = counted_target_coordinates.most_common(1)
        if duplication == 1:
            return None
        else:
            return duplicated_target_coordinates

    def process_board_movements(self, phase: int) -> None:
        board_movement_order = [DualSpeedConveyor, Conveyor, Rotator, Pusher]
        for current_board_movement_type in board_movement_order:
            # Build list of movement possibilities
            possible_movements: list[MovementPossibility] = []
            for movable in self.movables:
                board_element = self.elements[movable.coordinates]
                if isinstance(board_element, current_board_movement_type):
                    movement = board_element.board_movements(phase, movable)
                    if movement:
                        possible_movements.append(self._process_movement(movement, ignore_movable_collision=True))
                    else:
                        possible_movements.append(MovementPossibility.from_movable(phase, movable))
                else:
                    possible_movements.append(MovementPossibility.from_movable(phase, movable))
            # Repeatedly filter this list until no duplicate target coordinates remain
            while duplicated_coordinates := self._get_duplicated_target_coordinates(possible_movements):
                possible_movements = list(map(lambda m: m.cancel_if_target_coord_matches(duplicated_coordinates), possible_movements))
            # Now execute these movements if they aren't no-op
            for move in possible_movements:
                move.process()

    def process_robot_movements(self, round: int, phase: int) -> None:
        movements: list[Movement] = []
        for movable in self.movables:
            cards = movable.get_cards_for(round, phase)
            movements.extend([movement for card in cards for movement in Movement.from_card_definition(movable, phase, card)])
        for movement in sorted(movements, key=lambda m: m.priority):
            self.process_movement(movement)
