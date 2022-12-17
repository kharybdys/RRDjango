from roborally.board.element import basic


class BasicElement:

    def __init__(self):
        self.location: basic.BasicElement = None
        self.archive_marker: basic.BasicElement = None
        self.order_number: int = -1
        self.died_this_turn = False

    def paint(self):
        pass
