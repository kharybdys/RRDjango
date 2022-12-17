from collections import defaultdict

from django.forms import model_to_dict

from roborally.board.basic import Point
from roborally.board.element import conveyor, pusher, rotator, basic
from roborally.board.element.basic import BasicElement
from roborally.board.laser import Laser
from roborally.game import movement
from roborally.models import ScenarioBoard, BoardElement, ElementTypes, Direction


class BoardLoader:
    def __init__(self, scenario_board: ScenarioBoard):
        self.transform = Transform(scenario_board.turns, scenario_board.offset_x, scenario_board.offset_y)
        self.board_elements = {}
        self.walls = defaultdict(set)
        self.lasers = {}
        self._load_board(scenario_board.board_name)

    @staticmethod
    def _create_element(element_type: ElementTypes, direction: Direction = None) -> BasicElement:
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
            case ElementTypes.ROTATOR_COUNTER_CLOCKWISE:
                return rotator.CounterClockwiseRotator()
            case ElementTypes.REPAIR:
                return basic.RepairElement()
            case ElementTypes.OPTION:
                return basic.OptionElement()
            case ElementTypes.BASIC:
                return basic.BasicElement()
            case ElementTypes.HOLE:
                return basic.HoleElement()
            case ElementTypes.STARTING_1:
                return basic.StartingElement("1")
            case ElementTypes.STARTING_2:
                return basic.StartingElement("2")
            case ElementTypes.STARTING_3:
                return basic.StartingElement("3")
            case ElementTypes.STARTING_4:
                return basic.StartingElement("4")
            case ElementTypes.STARTING_5:
                return basic.StartingElement("5")
            case ElementTypes.STARTING_6:
                return basic.StartingElement("6")
            case ElementTypes.STARTING_7:
                return basic.StartingElement("7")
            case ElementTypes.STARTING_8:
                return basic.StartingElement("8")
            case _:
                raise Exception(f"{element_type} is unsupported as BoardElement")

    def _load_board(self, board_name: str) -> None:
        board = BoardElement.objects.filter(name=board_name)

        max_x = 0
        max_y = 0

        for board_element in board:
            max_x = max(max_x, board_element.x_coordinate)
            max_y = max(max_y, board_element.y_coordinate)

        trans_func = self.transform.transform_function(max_x, max_y)
        elements = map(trans_func,
                       map(model_to_dict, board.exclude(element_type__in=[ElementTypes.WALL, ElementTypes.LASER])))
        walls = map(trans_func, map(model_to_dict, board.filter(element_type=ElementTypes.WALL)))
        lasers = map(trans_func, map(model_to_dict, board.filter(element_type=ElementTypes.LASER)))

        for element in elements:
            self.board_elements[Point(element['x_coordinate'], element['y_coordinate'])] = self._create_element(element_type=element['element_type'], direction=element['direction'])

        for wall in walls:
            if wall['direction'] is None:
                raise Exception("Walls require a direction")
            self.walls[Point(wall['x_coordinate'], wall['y_coordinate'])].add(Direction(wall['direction']))

        for laser in lasers:
            if laser['direction'] is None:
                raise Exception("Lasers require a direction")
            laser_key = (Point(laser['x_coordinate'], laser['y_coordinate']), laser['direction'])
            if self.lasers.get(laser_key):
                self.lasers[laser_key].hits += 1
            else:
                self.lasers[laser_key] = Laser(Direction(laser['direction']))

        top_left = trans_func({'x_coordinate': 0, 'y_coordinate': 0, 'direction': 'NORTH'})
        bottom_right = trans_func({'x_coordinate': max_x, 'y_coordinate': max_y, 'direction': 'NORTH'})

        for x in range(min(top_left['x_coordinate'], bottom_right['x_coordinate']),
                       max(top_left['x_coordinate'], bottom_right['x_coordinate']) + 1):
            for y in range(min(top_left['y_coordinate'], bottom_right['y_coordinate']),
                           max(top_left['y_coordinate'], bottom_right['y_coordinate']) + 1):
                if Point(x, y) not in self.board_elements.keys():
                    self.board_elements[Point(x, y)] = self._create_element(ElementTypes.BASIC)


class Transform:

    def __init__(self, turns: int, x_offset: int, y_offset: int):
        self.turns = turns % 4  # should now be between 0 and 3
        self.x_offset = x_offset
        self.y_offset = y_offset

    @staticmethod
    def _coordinates_after_one_turn(max_x: int, max_y: int):
        def _turn(coordinates: Point) -> Point:
            nonlocal max_y
            nonlocal max_x
            new_coordinates = Point(max_y - coordinates.y, coordinates.x)
            temp = max_x
            max_x = max_y
            max_y = temp
            return new_coordinates

        return _turn

    def _turn_coordinate(self, coordinates: Point, max_x: int, max_y: int) -> Point:
        new_coordinates = coordinates
        turn = self._coordinates_after_one_turn(max_x, max_y)
        for _ in range(self.turns):
            new_coordinates = turn(new_coordinates)
        return new_coordinates

    def transform_function(self, max_x: int, max_y: int):
        def transform(data: dict):
            result = data.copy()
            new_coordinates = self._turn_coordinate(Point(result['x_coordinate'], result['y_coordinate']), max_x, max_y)
            result['x_coordinate'] = new_coordinates.x
            result['y_coordinate'] = new_coordinates.y
            result['x_coordinate'] += self.x_offset
            result['y_coordinate'] += self.y_offset
            result['direction'] = movement.get_to_direction(result['direction'], self.turns)
            return result
        return transform
