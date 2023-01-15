from abc import ABC, abstractmethod
from typing import Iterable
from roborally.game.direction import Direction
from roborally.game.events import EventType


class MovableModel(ABC):
    x_coordinate: int = -1
    y_coordinate: int = -1
    archive_x_coordinate: int = -1
    archive_y_coordinate: int = -1
    facing_direction: Direction = None

    @property
    def order_number(self) -> int:
        return 0


class BotModel(MovableModel):
    damage: int = 0

    @abstractmethod
    def get_cards_for(self, round: int, phase: int):
        pass

    @abstractmethod
    def log_event(self, phase: int, event_type: EventType, other_model: MovableModel, **kwargs):
        pass


class FlagModel(MovableModel):
    @abstractmethod
    def save(self):
        pass


class GameModel(ABC):

    @abstractmethod
    def get_scenario_data_provider(self):
        pass

    @property
    def bots(self) -> Iterable[BotModel]:
        return []

    @property
    def flags(self) -> Iterable[FlagModel]:
        return []
