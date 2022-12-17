from collections import defaultdict

from roborally.board.basic import Point
from roborally.board.element.basic import BasicElement
from roborally.board.loader import BoardLoader
from roborally.game.bot import Bot
from roborally.models import ScenarioBoard as ScenarioModel, ScenarioFlag, Direction
from roborally.board.element import basic
from roborally.board.laser import Laser
from roborally.game import movement
from roborally.game.flag import Flag
from roborally.utils.codec import SerializationMixin


class Scenario(SerializationMixin):

    def __init__(self, scenario_name, load_flags=False):
        self.y_size = 0
        self.x_size = 0
        self.elements: dict[Point, BasicElement] = {}
        self.walls: dict[Point, set[Direction]] = defaultdict(set)
        self.lasers: dict[tuple[Point, Direction], Laser] = {}
        self.flags: dict[Point, Flag] = {}
        self.bots: dict[Point, Bot] = {}
        boards = ScenarioModel.objects.filter(name=scenario_name)
        for board in boards:
            self._add_board(board)

        self._determine_size()
        if load_flags:
            self._add_flags(scenario_name)
        self._fill_neighbours()
        self._validate()

    def add_flag(self, flag: Flag):
        self.flags[flag.coordinates] = flag

    def add_bot(self, bot: Bot):
        self.bots[bot.coordinates] = bot

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

    def _add_flags(self, scenario_name: str):
        flags = ScenarioFlag.objects.filter(name=scenario_name)
        for flag in flags:
            self.add_flag(Flag(flag))

    def _add_board(self, board: ScenarioModel):
        loader = BoardLoader(board)
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
                    for direction in Direction.values:
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
                wall_data = {self.KEY_DIRECTION: direction}
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
            if movement.get_to_direction(direction, 2) in self.walls[new_coordinates]:
                return coordinates
            else:
                return self.determine_laser_end(new_coordinates, direction, ignore_bots)
