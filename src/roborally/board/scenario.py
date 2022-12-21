from collections import defaultdict

import roborally.game.direction
from roborally.board.basic import Point
from roborally.board.element import basic
from roborally.board.laser import Laser
from roborally.board.data.loader import BoardLoader, ScenarioDataProvider
from roborally.game.basic import BasicMovableElement
from roborally.game.direction import Direction
from roborally.game.bot import Bot
from roborally.game.events import WallCollisionEvent, BotCollisionEvent, MovableElementKilledEvent
from roborally.game.flag import Flag
from roborally.game.movement import Movement
from roborally.utils.codec import SerializationMixin


class Scenario(SerializationMixin):

    def __init__(self, scenario_data_provider: ScenarioDataProvider, load_flags: bool = False):
        self.y_size = 0
        self.x_size = 0
        self.elements: dict[Point, basic.BasicElement] = {}
        self.walls: dict[Point, set[Direction]] = defaultdict(set)
        self.lasers: dict[tuple[Point, Direction], Laser] = {}
        self.flags: dict[Point, Flag] = {}
        self.bots: dict[Point, Bot] = {}
        for loader in scenario_data_provider.get_loader_for_boards():
            self._add_board(loader)

        self._determine_size()
        if load_flags:
            for flag in scenario_data_provider.flags:
                self.add_flag(Flag(flag))
        self._fill_neighbours()
        self._validate()

    def add_flag(self, flag: Flag):
        self.flags[flag.coordinates] = flag

    def add_bot(self, bot: Bot):
        self.bots[bot.coordinates] = bot

    def add_movable(self, movable: BasicMovableElement):
        if isinstance(movable, Bot):
            self.add_bot(movable)
        elif isinstance(movable, Flag):
            self.add_flag(movable)
        else:
            raise ValueError(f"Unsupported type of movable: {movable}")

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
        pass

    def to_data(self) -> dict:
        board_data = {'factor': basic.DRAW_MAGNIFICATION_FACTOR,
                      'width': self.x_size,
                      'height': self.y_size,
                      'elements': [],
                      'walls': [],
                      'lasers': [],
                      'flags': [],
                      'bots': []
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
            laser_data['laser_path'] = list(map(lambda p: p.to_data(), self._generate_laser_path(coordinates, laser_end)))
            board_data['lasers'].append(laser_data)

        for coordinates, flag in self.flags.items():
            flag_data = flag.to_data()
            flag_data.update(coordinates.to_data())
            board_data['flags'].append(flag_data)

        for coordinates, bot in self.bots.items():
            bot_data = bot.to_data()
            bot_data.update(coordinates.to_data())
            board_data['bots'].append(bot_data)

        return board_data

    def determine_laser_end(self, coordinates: Point, direction: Direction, ignore_bots: bool) -> Point:
        # TODO: Also ignore originating bot
        if direction in self.walls[coordinates] or (not ignore_bots and coordinates in self.bots.keys()):
            return coordinates
        else:
            new_coordinates = coordinates.neighbour(direction)
            if roborally.game.direction.get_to_direction(direction, 2) in self.walls[new_coordinates]:
                return coordinates
            else:
                return self.determine_laser_end(new_coordinates, direction, ignore_bots)

    def update_movable_coordinates_and_direction(self, movable: BasicMovableElement, new_coordinates: Point, new_direction: Direction):
        match movable:
            case Bot():
                movables = self.bots
            case Flag():
                movables = self.flags
            case _:
                raise ValueError(f"Updating movable of type {movable.__class__} not supported")
        self._update_movable_coordinates_and_direction(movable, new_coordinates, new_direction, movables)

    @staticmethod
    def _update_movable_coordinates_and_direction(movable: BasicMovableElement, new_coordinates: Point, new_direction: Direction, movables: dict[Point, BasicMovableElement]):
        # movable should be found in the scenario at the current movable coordinates, remove it from there.
        if movables[movable.coordinates] == movable:
            del movables[movable.coordinates]
            movable.update_coordinates_and_direction(new_coordinates, new_direction)
            movables[new_coordinates] = movable
        else:
            raise Exception(f"Movable {movable.order_number} not found on expected coordinates: {movable.coordinates}")

    def all_board_movements(self, phase: int) -> list[Movement]:
        result = []
        for (coordinates, flag) in self.flags.items():
            result.extend(self.elements[coordinates].board_movements(phase, flag))
        for (coordinates, bot) in self.bots.items():
            result.extend(self.elements[coordinates].board_movements(phase, bot))
        return result

    def process_movement(self, movement: Movement):
        current_coordinates = movement.moved_object.coordinates
        if movement.direction in self.walls[current_coordinates]:
            raise WallCollisionEvent
        new_coordinates = current_coordinates
        for _ in range(0, movement.steps):
            new_coordinates = new_coordinates.neighbour(movement.direction)
        if new_coordinates in self.bots.keys():
            # TODO: This is too simplistic, pushing (if movement_type is robot) is missing
            raise BotCollisionEvent
        if self.elements[current_coordinates].get_neighbour(movement.direction).KILLS:
            # TODO: Handle movable being killed
            raise MovableElementKilledEvent
        new_direction = movement.moved_object.facing_direction.turn(movement.turns)
        self.update_movable_coordinates_and_direction(movement.moved_object, new_coordinates, new_direction)
