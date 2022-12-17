from roborally.models import ElementTypes

# parameters for drawing a board on the web
FACTOR = 6
KEY_ELEMENT_TYPE = 'element_type'


class BasicElement:

    def __init__(self):
        self.type = ElementTypes.BASIC
        self.neighbours = {}
        self.walls = {}

    def is_start(self):
        return self.type in [ElementTypes.STARTING_1,
                             ElementTypes.STARTING_2,
                             ElementTypes.STARTING_3,
                             ElementTypes.STARTING_4,
                             ElementTypes.STARTING_5,
                             ElementTypes.STARTING_6,
                             ElementTypes.STARTING_7,
                             ElementTypes.STARTING_8]

    def to_data(self):
        return {KEY_ELEMENT_TYPE: self.type}

    def symbol(self):
        match self.type:
            case ElementTypes.STARTING_1:
                return '1'
            case ElementTypes.STARTING_2:
                return '2'
            case ElementTypes.STARTING_3:
                return '3'
            case ElementTypes.STARTING_4:
                return '4'
            case ElementTypes.STARTING_5:
                return '5'
            case ElementTypes.STARTING_6:
                return '6'
            case ElementTypes.STARTING_7:
                return '7'
            case ElementTypes.STARTING_8:
                return '8'
            case _:
                return None

    # to be overridden
    def board_movements(self, phase):
        return []

    def get_neighbour(self, direction):
        return self.neighbours.get(direction)

    def set_neighbour(self, direction, element):
        self.neighbours[direction] = element

    def neighbours_completed(self):
        pass

    def has_wall(self, direction):
        return direction in self.walls.keys()

    def set_wall(self, direction, wall=True):
        self.walls[direction] = wall
