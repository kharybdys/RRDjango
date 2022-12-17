from collections import defaultdict
from django.forms import model_to_dict
from roborally.models import BoardElement, Scenario, ScenarioFlag, ElementTypes, Direction
from roborally.board.element import conveyor, pusher, rotator
from roborally.board.element import basic
from roborally.board.laser import Laser
from roborally.game import movement
from roborally.game.flag import Flag


def _generate_coordinates_list(start_x, start_y, end_x, end_y):
    x_range = list(range(min(start_x, end_x), max(start_x, end_x) + 1))  # include end_x
    y_range = list(range(min(start_y, end_y), max(start_y, end_y) + 1))  # include end_y
    x_range.extend([end_x] * (len(y_range) - len(x_range)))
    y_range.extend([end_y] * (len(x_range) - len(y_range)))
    return [dict(zip(['x', 'y'], d)) for d in zip(x_range, y_range)]


def create_element(element_type, direction=None):
    match element_type:
        case ElementTypes.WALL:
            raise Exception("Wall is not an element")
        case ElementTypes.LASER:
            raise Exception("Laser is not an element")
        case ElementTypes.DUAL_CONVEYOR:
            return conveyor.DualSpeedConveyor(end_direction=direction)
        case ElementTypes.SINGLE_CONVEYOR:
            return conveyor.SingleSpeedConveyor(end_direction=direction)
        case ElementTypes.PUSHER_135:
            return pusher.Pusher135(direction=direction)
        case ElementTypes.PUSHER_24:
            return pusher.Pusher24(direction=direction)
        case ElementTypes.ROTATOR_CLOCKWISE:
            return rotator.ClockwiseRotator()
        case ElementTypes.ROTATOR_COUNTERCLOCKWISE:
            return rotator.CounterClockwiseRotator()
        case _:
            basic_element = basic.BasicElement()
            basic_element.type = element_type
            return basic_element


# Defines the relation between the coordinate system and the directions
# 0,0 will be top-left as that is what fabric.js expects
def _get_coords(direction, coordinates):
    match direction:
        case Direction.SOUTH:
            return coordinates[0], coordinates[1] + 1
        case Direction.NORTH:
            return coordinates[0], coordinates[1] - 1
        case Direction.WEST:
            return coordinates[0] - 1, coordinates[1]
        case Direction.EAST:
            return coordinates[0] + 1, coordinates[1]


def _single_turn_coordinate(max_x, max_y):

    def _turn(coordinates):
        nonlocal max_y
        nonlocal max_x
        new_coordinates = (max_y - coordinates[1], coordinates[0])
        temp = max_x
        max_x = max_y
        max_y = temp
        return new_coordinates

    return _turn


class Transform:

    def __init__(self, turns, x_offset, y_offset):
        self.turns = turns % 4  # should now be between 0 and 3
        self.x_offset = x_offset
        self.y_offset = y_offset

    def _turn_coordinate(self, coordinates, max_x, max_y):
        new_coordinates = coordinates
        turn = _single_turn_coordinate(max_x, max_y)
        for _ in range(self.turns):
            new_coordinates = turn(new_coordinates)
        return new_coordinates

    def transform_function(self, max_x, max_y):
        def transform(data: dict):
            result = data.copy()
            result['x_coordinate'], result['y_coordinate'] = self._turn_coordinate((result['x_coordinate'], result['y_coordinate']), max_x, max_y)
            result['x_coordinate'] += self.x_offset
            result['y_coordinate'] += self.y_offset
            result['direction'] = movement.get_to_direction(result['direction'], self.turns)
            return result
        return transform


def add_board(board_name, transform: Transform):
    board = BoardElement.objects.filter(name=board_name)

    max_x = 0
    max_y = 0

    for board_element in board:
        max_x = max(max_x, board_element.x_coordinate)
        max_y = max(max_y, board_element.y_coordinate)

    trans_func = transform.transform_function(max_x, max_y)
    elements = map(trans_func, map(model_to_dict, board.exclude(element_type__in=[ElementTypes.WALL, ElementTypes.LASER])))
    walls = map(trans_func, map(model_to_dict, board.filter(element_type=ElementTypes.WALL)))
    lasers = map(trans_func, map(model_to_dict, board.filter(element_type=ElementTypes.LASER)))

    result_elements = {}
    for element in elements:
        result_elements[(element['x_coordinate'],
                         element['y_coordinate'])] = create_element(element_type=element['element_type'],
                                                                    direction=element['direction'])

    result_walls = defaultdict(set)
    for wall in walls:
        if wall['direction'] is None:
            raise Exception("Walls require a direction")
        result_walls[(wall['x_coordinate'],
                      wall['y_coordinate'])].add(wall['direction'])

    result_lasers = {}
    for laser in lasers:
        if laser['direction'] is None:
            raise Exception("Lasers require a direction")
        if result_lasers.get((laser['x_coordinate'], laser['y_coordinate'], laser['direction'])):
            result_lasers[(laser['x_coordinate'], laser['y_coordinate'], laser['direction'])].hits += 1
        else:
            result_lasers[(laser['x_coordinate'], laser['y_coordinate'], laser['direction'])] = Laser(laser['direction'])

    top_left = trans_func({'x_coordinate': 0, 'y_coordinate': 0, 'direction': 'NORTH'})
    bottom_right = trans_func({'x_coordinate': max_x, 'y_coordinate': max_y, 'direction': 'NORTH'})

    for x in range(min(top_left['x_coordinate'], bottom_right['x_coordinate']),
                   max(top_left['x_coordinate'], bottom_right['x_coordinate']) + 1):
        for y in range(min(top_left['y_coordinate'], bottom_right['y_coordinate']),
                       max(top_left['y_coordinate'], bottom_right['y_coordinate']) + 1):
            if (x, y) not in result_elements:
                result_elements[(x, y)] = create_element(ElementTypes.BASIC)
    return result_elements, result_walls, result_lasers


class Board:

    def __init__(self, scenario_name, load_flags = False):
        self.y_size = 0
        self.x_size = 0
        self.elements = {}
        self.walls = defaultdict(set)
        self.lasers = {}
        self.flags = {}
        self.bots = {}
        boards = Scenario.objects.filter(name=scenario_name)
        for board in boards:
            self._add_board(board.board_name, Transform(board.turns, board.offset_x, board.offset_y))

        self._determine_size()
        if load_flags:
            self._add_flags(scenario_name)
        self._fill_neighbours()
        self._validate()

    def _add_flags(self, scenario_name):
        flags = ScenarioFlag.objects.filter(name=scenario_name)
        for flag in flags:
            self.flags[(flag.x_coordinate, flag.y_coordinate)] = Flag(flag)

    def _add_board(self, board_name, transform: Transform):
        result_elements, result_walls, result_lasers = add_board(board_name, transform)
        self.elements.update(result_elements)
        self.walls.update(result_walls)
        self.lasers.update(result_lasers)

    def _determine_size(self):
        self.x_size = 0
        self.y_size = 0
        for (x, y) in self.elements.keys():
            self.x_size = max(self.x_size, x)
            self.y_size = max(self.y_size, y)

        for (x, y, _) in self.lasers.keys():
            self.x_size = max(self.x_size, x)
            self.y_size = max(self.y_size, y)

        for (x, y) in self.walls.keys():
            self.x_size = max(self.x_size, x)
            self.y_size = max(self.y_size, y)

        self.x_size += 1
        self.y_size += 1

    def _fill_neighbours(self):
        void = create_element('VOID')
        for x in range(0, self.x_size):
            for y in range(0, self.y_size):
                current_element = self.elements.get((x, y))
                if current_element:
                    for direction in Direction.values:
                        neighbour = self.elements.get(_get_coords(direction, (x, y)), void)
                        current_element.set_neighbour(direction, neighbour)
                    current_element.neighbours_completed()

    def _validate(self):
        pass

    def to_data(self) -> dict:
        board_data = {'factor': basic.FACTOR,
                      'width': self.x_size,
                      'height': self.y_size,
                      'elements': [],
                      'walls': [],
                      'lasers': [],
                      'flags': [],
                      'bots': []
                      }

        for coordinates, element in sorted(self.elements.items()):
            element_data = element.to_data()
            element_data['x'] = coordinates[0]
            element_data['y'] = coordinates[1]
            board_data['elements'].append(element_data)

        for coordinates, directions in self.walls.items():
            for direction in directions:
                wall_data = {'direction': direction,
                             'x': coordinates[0],
                             'y': coordinates[1]}
                board_data['walls'].append(wall_data)

        for key, laser in self.lasers.items():
            end_x, end_y = self.determine_laser_end((key[0], key[1]), key[2], True)
            laser_data = laser.to_data()
            laser_data['x'] = key[0]
            laser_data['y'] = key[1]
            laser_data['laser_path'] = _generate_coordinates_list(key[0], key[1], end_x, end_y)
            board_data['lasers'].append(laser_data)

        for coordinates, flag in self.flags.items():
            flag_data = flag.to_data()
            flag_data['x'] = coordinates[0]
            flag_data['y'] = coordinates[1]
            board_data['flags'].append(flag_data)

        return board_data

    # assumes this is either horizontal or vertical (ie the x's are equal or the y's are)
    def determine_laser_end(self, coordinates, direction, ignore_bots):
        # TODO: Also ignore originating bot
        if direction in self.walls[coordinates] or (not ignore_bots and coordinates in self.bots.keys()):
            return coordinates
        else:
            new_coordinates = _get_coords(direction, coordinates)
            if movement.get_to_direction(direction, 2) in self.walls[new_coordinates]:
                return coordinates
            else:
                return self.determine_laser_end(new_coordinates, direction, ignore_bots)
