from abc import ABC, abstractmethod

from roborally.board.element import basic

KEY_SYMBOL = 'symbol'


class BasicMovableElement(ABC):

    def __init__(self):
        self.location: basic.BasicElement
        self.archive_marker: basic.BasicElement
        self.order_number: int = -1
        self.died_this_turn = False

    @abstractmethod
    def to_data(self):
        pass
