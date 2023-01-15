from typing import Iterable

from django.db import models

from roborally.board.data.data_django import DjangoScenarioDataProvider
from roborally.game.models import GameModel, FlagModel, BotModel
from roborally.models.abc import AbstractModelMeta
from roborally.models.scenario import ScenarioName


class GameStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE'
    CALCULATING = 'CALCULATING'
    FINISHED = 'FINISHED'


class Game(models.Model, GameModel, metaclass=AbstractModelMeta):
    name = models.CharField(max_length=250, unique=True)
    scenario_name = models.CharField(choices=ScenarioName.choices, max_length=250)
    current_round = models.IntegerField(default=0)
    status = models.CharField(choices=GameStatus.choices,
                              max_length=15,
                              default=GameStatus.CALCULATING
                              )
    created_by = models.CharField(max_length=250, default='internal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=250, default='internal')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}[{self.id}]'

    def get_scenario_data_provider(self):
        return DjangoScenarioDataProvider(self.scenario_name)

    @property
    def bots(self) -> Iterable[BotModel]:
        return self.bot_set

    @property
    def flags(self) -> Iterable[FlagModel]:
        return self.flag_set
