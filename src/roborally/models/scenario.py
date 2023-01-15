from django.db import models

from roborally.board.data.loader import ElementTypes
from roborally.game.direction import Direction


class ScenarioName(models.TextChoices):
    MOVING_TARGETS = "MOVING_TARGETS",
    AGAINST_THE_GRAIN = "AGAINST_THE_GRAIN",
    TRICKSY = "TRICKSY",
    ISLAND_KING = "ISLAND_KING",
    ODDEST_SEA = "ODDEST_SEA",
    ROBOT_STEW = "ROBOT_STEW",
    LOST_BEARINGS = "LOST_BEARINGS",
    WHIRLWIND_TOUR = "WHIRLWIND_TOUR",
    VAULT_ASSAULT = "VAULT_ASSAULT",
    PILGRIMAGE = "PILGRIMAGE",
    DEATH_TRAP = "DEATH_TRAP",
    AROUND_THE_WORLD = "AROUND_THE_WORLD",
    BLOODBATH_CHESS = "BLOODBATH_CHESS",
    TWISTER = "TWISTER",
    CHOP_SHOP_CHALLENGE = "CHOP_SHOP_CHALLENGE",
    ISLAND_HOP = "ISLAND_HOP",
    DIZZY_DASH = "DIZZY_DASH",
    CHECKMATE = "CHECKMATE",
    RISKY_EXCHANGE = "RISKY_EXCHANGE",
    SET_TO_KILL = "SET_TO_KILL",
    FACTORY_REJECTS = "FACTORY_REJECTS",
    OPTION_WORLD = "OPTION_WORLD",
    TIGHT_COLLAR = "TIGHT_COLLAR",
    BALL_LIGHTNING = "BALL_LIGHTNING",
    DAY_OF_THE_SUPERBOT = "DAY_OF_THE_SUPERBOT",
    INTERFERENCE = "INTERFERENCE",
    FLAG_FRY = "FLAG_FRY",
    FRENETIC_FACTORY = "FRENETIC_FACTORY"
    MARATHON_MADNESS = "MARATHON_MADNESS",
    TANDEM_CARNAGE = "TANDEM_CARNAGE",
    ALL_FOR_ONE = "ALL_FOR_ONE"
    CAPTURE_THE_FLAG = "CAPTURE_THE_FLAG",
    TOGGLE_BOGGLE = "TOGGLE_BOGGLE",
    WAR_ZONE = "WAR_ZONE"


class BoardName(models.TextChoices):
    STARTING_BOARD_1 = "STARTING_BOARD_1",
    STARTING_BOARD_2 = "STARTING_BOARD_2",
    MAELSTROM = "MAELSTROM",
    SPIN_ZONE = "SPIN_ZONE",
    VAULT = "VAULT",
    CROSS = "CROSS",
    CHESS = "CHESS",
    CHOP_SHOP = "CHOP_SHOP",
    ISLAND = "ISLAND",
    EXCHANGE = "EXCHANGE"


class ScenarioBoard(models.Model):
    name = models.CharField(choices=ScenarioName.choices,
                            max_length=50)
    turns = models.IntegerField(default=0)
    offset_x = models.IntegerField(default=0)
    offset_y = models.IntegerField(default=0)
    board_name = models.CharField(choices=BoardName.choices,
                                  max_length=20)


class ScenarioFlag(models.Model):
    name = models.CharField(choices=ScenarioName.choices,
                            max_length=50)
    x_coordinate = models.IntegerField(default=-1)
    y_coordinate = models.IntegerField(default=-1)
    order_number = models.IntegerField(default=0)


class BoardElement(models.Model):
    name = models.CharField(choices=BoardName.choices,
                            max_length=20)
    element_type = models.CharField(choices=ElementTypes.get_choices(),
                                    max_length=50)
    x_coordinate = models.IntegerField(default=-1)
    y_coordinate = models.IntegerField(default=-1)
    direction = models.CharField(choices=Direction.get_choices(),
                                 max_length=5,
                                 null=True,
                                 blank=True)

    def to_dict(self):
        return {'name': self.name,
                'element_type': ElementTypes(self.element_type) if self.element_type else None,
                'x_coordinate': self.x_coordinate,
                'y_coordinate': self.y_coordinate,
                'direction': Direction(self.direction) if self.direction else None
                }
