from roborally.board.scenario import Scenario
from roborally.game.bot import Bot
from roborally.game.flag import Flag
from roborally.models import Game as GameModel


class Game:
    def __init__(self, game_id: int):
        self.model = GameModel.objects.get(pk=game_id)
        self.scenario = Scenario(scenario_name=self.model.scenario_name, load_flags=False)
        self._load_flags()
        self._load_bots()

    def _load_flags(self):
        flags = self.model.flag_set
        for flag in flags:
            self.scenario.add_flag(Flag(flag))

    def _load_bots(self):
        bots = self.model.bot_set
        for bot in bots:
            self.scenario.add_bot(Bot(bot))
