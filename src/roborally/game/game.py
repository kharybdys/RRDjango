from roborally.board.data.data_db import ScenarioDataProvider
from roborally.board.scenario import Scenario
from roborally.game.bot import Bot
from roborally.game.events import EventException
from roborally.game.flag import Flag
from roborally.game.movement import Movement
from roborally.models import Game as GameModel


class Game:
    def __init__(self, game_id: int):
        self.model = GameModel.objects.get(pk=game_id)
        scenario_data_provider = ScenarioDataProvider(self.model.scenario_name)
        self.scenario = Scenario(scenario_data_provider=scenario_data_provider, load_flags=False)
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

    def process_movements(self, phase: int):
        self.process_robot_movements(phase)
        self.process_board_movements(phase)

    def process_board_movements(self, phase: int):
        # TODO: Doesn't handle moving from conveyor onto pusher/rotator
        self._process_movements(self.scenario.all_board_movements(phase))

    def process_robot_movements(self, phase: int):
        pass

    def _process_movements(self, movements: list[Movement]):
        for movement in sorted(movements, key=lambda m: m.priority):
            try:
                self.scenario.process_movement(movement)
            except EventException as e:
                # TODO: Do something more serious with the event
                print(e)

    # To process any movement on a bot or flag
    # get the movement objects together with the bot or flag they apply to, either from cards or from board
    # for each movement (maybe in a specific order, priority?):
    #   try to apply it to the bot/flag, given the location of bot/flag on the board & board particulars
    #     this might result in: updated coordinates/directions on bot/flag (collisions -> also on other bots)
    #                           events logged
