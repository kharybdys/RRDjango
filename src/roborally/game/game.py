from roborally.board.scenario import Scenario
from roborally.game.bot import Bot
from roborally.game.flag import Flag
from roborally.game.movement import Movement
from roborally.game.models import GameModel


class Game:
    def __init__(self, game: GameModel):
        self.model = game
        self.phase = 1
        self.scenario = Scenario(scenario_data_provider=self.model.get_scenario_data_provider(), load_flags=False)
        self._load_flags()
        self._load_bots()

    def increase_phase(self):
        self.phase += 1

    def _load_flags(self):
        flags = self.model.flags
        for flag in flags:
            self.scenario.add_movable(Flag(flag))

    def _load_bots(self):
        bots = self.model.bots
        for bot in bots:
            self.scenario.add_movable(Bot(bot))

    def process_phase(self):
        self.process_robot_movements()
        self.process_board_movements()
        self.process_laser_shots()
        self.increase_phase()

    def process_board_movements(self):
        self.scenario.process_board_movements(self.phase)

    def process_robot_movements(self):
        self.scenario.process_robot_movements(self.model.round, self.phase)

    def process_laser_shots(self):
        pass

    def _process_movements_by_priority(self, movements: list[Movement]):
        for movement in sorted(movements, key=lambda m: m.priority):
            self.scenario.process_movement(movement)
