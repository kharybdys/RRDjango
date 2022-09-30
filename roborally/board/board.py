from collections import defaultdict
from roborally.models import BoardElement, ElementTypes, Direction
from roborally.board.element import basic, conveyor, pusher, rotator
from roborally.board.laser import Laser
from roborally.game import movement
from copy import deepcopy


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


class Board:

    def __init__(self, board_name):
        self.elements = {}
        self.walls = defaultdict(set)
        self.lasers = {}
        self.bots = {}
        self.x_size = 0
        self.y_size = 0

        board = BoardElement.objects.filter(name=board_name)
        elements = board.exclude(element_type__in=[ElementTypes.WALL, ElementTypes.LASER])
        walls = board.filter(element_type=ElementTypes.WALL)
        lasers = board.filter(element_type=ElementTypes.LASER)

        for element in elements:
            self.x_size = max(self.x_size, element.x_coordinate)
            self.y_size = max(self.y_size, element.y_coordinate)
            self.elements[(element.x_coordinate,
                           element.y_coordinate)] = create_element(element_type=element.element_type,
                                                                   direction=element.direction)

        for wall in walls:
            if wall.direction is None:
                raise Exception("Walls require a direction")
            self.x_size = max(self.x_size, wall.x_coordinate)
            self.y_size = max(self.y_size, wall.y_coordinate)
            self.walls[(wall.x_coordinate,
                        wall.y_coordinate)].add(wall.direction)

        for laser in lasers:
            if laser.direction is None:
                raise Exception("Lasers require a direction")
            self.x_size = max(self.x_size, laser.x_coordinate)
            self.y_size = max(self.y_size, laser.y_coordinate)
            if self.lasers.get((laser.x_coordinate, laser.y_coordinate, laser.direction)):
                self.lasers[(laser.x_coordinate, laser.y_coordinate, laser.direction)].hits += 1
            else:
                self.lasers[(laser.x_coordinate, laser.y_coordinate, laser.direction)] = Laser(laser.direction, self)

        self.x_size += 1
        self.y_size += 1
        self.fill_with_basics()
        self.fill_neighbours()
        self.validate()

    def fill_with_basics(self):
        for x in range(0, self.x_size):
            for y in range(0, self.y_size):
                if (x, y) not in self.elements:
                    self.elements[(x, y)] = create_element(ElementTypes.BASIC)

    def fill_neighbours(self):
        void = create_element('VOID')
        for x in range(0, self.x_size):
            for y in range(0, self.y_size):
                current_element = self.elements[(x, y)]
                for direction in Direction.values:
                    neighbour = self.elements.get(_get_coords(direction, (x, y)), void)
                    current_element.set_neighbour(direction, neighbour)
                current_element.neighbours_completed()

    def validate(self):
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
        return board_data

    # assumes this is either horizontal or vertical (ie the x's are equal or the y's are)
    def determine_laser_end(self, coordinates, direction, ignore_bots):
        # TODO: Also ignore originating bot
        if direction in self.walls[coordinates] or (not ignore_bots and coordinates in self.bots.keys()):
            return coordinates
        else:
            new_coordinates = _get_coords(direction, coordinates);
            if movement.get_to_direction(direction, 2) in self.walls[new_coordinates]:
                return coordinates
            else:
                return self.determine_laser_end(new_coordinates, direction, ignore_bots)
