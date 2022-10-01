from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, ModelMultipleChoiceField


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


class ElementTypes(models.TextChoices):
    BASIC = 'BASIC',
    STARTING_1 = 'STARTING_1',
    STARTING_2 = 'STARTING_2',
    STARTING_3 = 'STARTING_3',
    STARTING_4 = 'STARTING_4',
    STARTING_5 = 'STARTING_5',
    STARTING_6 = 'STARTING_6',
    STARTING_7 = 'STARTING_7',
    STARTING_8 = 'STARTING_8',
    REPAIR = 'REPAIR',
    OPTION = 'OPTION',
    HOLE = 'HOLE',
    SINGLE_CONVEYOR = 'SINGLE_CONVEYOR',
    DUAL_CONVEYOR = 'DUAL_CONVEYOR',
    PUSHER_135 = 'PUSHER_135',
    PUSHER_24 = 'PUSHER_24',
    ROTATOR_CLOCKWISE = 'ROTATOR_CLOCKWISE',
    ROTATOR_COUNTERCLOCKWISE = 'ROTATOR_COUNTERCLOCKWISE',
    WALL = 'WALL',
    LASER = 'LASER'


class GameStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE'
    CALCULATING = 'CALCULATING'
    FINISHED = 'FINISHED'


class CardStatus(models.TextChoices):
    INITIAL = 'INITIAL'
    FINAL = 'FINAL'
    LOCKED = 'LOCKED'
    FLYWHEEL = 'FLYWHEEL'


class Direction(models.TextChoices):
    NORTH = 'NORTH'
    EAST = 'EAST'
    SOUTH = 'SOUTH'
    WEST = 'WEST'


class CardDefinition(models.TextChoices):
    MC_10 = 'MC_10'
    MC_20 = 'MC_20'
    MC_30 = 'MC_30'
    MC_40 = 'MC_40'
    MC_50 = 'MC_50'
    MC_60 = 'MC_60'
    MC_70 = 'MC_70'
    MC_80 = 'MC_80'
    MC_90 = 'MC_90'
    MC_100 = 'MC_100'
    MC_110 = 'MC_110'
    MC_120 = 'MC_120'
    MC_130 = 'MC_130'
    MC_140 = 'MC_140'
    MC_150 = 'MC_150'
    MC_160 = 'MC_160'
    MC_170 = 'MC_170'
    MC_180 = 'MC_180'
    MC_190 = 'MC_190'
    MC_200 = 'MC_200'
    MC_210 = 'MC_210'
    MC_220 = 'MC_220'
    MC_230 = 'MC_230'
    MC_240 = 'MC_240'
    MC_250 = 'MC_250'
    MC_260 = 'MC_260'
    MC_270 = 'MC_270'
    MC_280 = 'MC_280'
    MC_290 = 'MC_290'
    MC_300 = 'MC_300'
    MC_310 = 'MC_310'
    MC_320 = 'MC_320'
    MC_330 = 'MC_330'
    MC_340 = 'MC_340'
    MC_350 = 'MC_350'
    MC_360 = 'MC_360'
    MC_370 = 'MC_370'
    MC_380 = 'MC_380'
    MC_390 = 'MC_390'
    MC_400 = 'MC_400'
    MC_410 = 'MC_410'
    MC_420 = 'MC_420'
    MC_430 = 'MC_430'
    MC_440 = 'MC_440'
    MC_450 = 'MC_450'
    MC_460 = 'MC_460'
    MC_470 = 'MC_470'
    MC_480 = 'MC_480'
    MC_490 = 'MC_490'
    MC_500 = 'MC_500'
    MC_510 = 'MC_510'
    MC_520 = 'MC_520'
    MC_530 = 'MC_530'
    MC_540 = 'MC_540'
    MC_550 = 'MC_550'
    MC_560 = 'MC_560'
    MC_570 = 'MC_570'
    MC_580 = 'MC_580'
    MC_590 = 'MC_590'
    MC_600 = 'MC_600'
    MC_610 = 'MC_610'
    MC_620 = 'MC_620'
    MC_630 = 'MC_630'
    MC_640 = 'MC_640'
    MC_650 = 'MC_650'
    MC_660 = 'MC_660'
    MC_670 = 'MC_670'
    MC_680 = 'MC_680'
    MC_690 = 'MC_690'
    MC_700 = 'MC_700'
    MC_710 = 'MC_710'
    MC_720 = 'MC_720'
    MC_730 = 'MC_730'
    MC_740 = 'MC_740'
    MC_750 = 'MC_750'
    MC_760 = 'MC_760'
    MC_770 = 'MC_770'
    MC_780 = 'MC_780'
    MC_790 = 'MC_790'
    MC_800 = 'MC_800'
    MC_810 = 'MC_810'
    MC_820 = 'MC_820'
    MC_830 = 'MC_830'
    MC_840 = 'MC_840'


class EventType(models.TextChoices):
    BOT_PUSHES = 'BOT_PUSHES'
    CONVEYORBELT_STALL = 'CONVEYORBELT_STALL'
    BOT_SHOOTS = 'BOT_SHOOTS'
    BOARD_SHOOTS = 'BOARD_SHOOTS'
    BOT_DIES_DAMAGE = 'BOT_DIES_DAMAGE'
    BOT_DIES_HOLE = 'BOT_DIES_HOLE'
    ARCHIVE_MARKER_MOVED = 'ARCHIVE_MARKER_MOVED'
    POWER_DOWN = 'POWER_DOWN'
    BOT_HITS_WALL = 'BOT_HITS_WALL'
    BOT_HITS_UNMOVABLE_BOT = 'BOT_HITS_UNMOVABLE_BOT'


class Scenario(models.Model):
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
    element_type = models.CharField(choices=ElementTypes.choices,
                                    max_length=50)
    x_coordinate = models.IntegerField(default=-1)
    y_coordinate = models.IntegerField(default=-1)
    direction = models.CharField(choices=Direction.choices,
                                 max_length=5,
                                 null=True,
                                 blank=True)


class Binary(models.Model):
    data = models.BinaryField()  # TODO: See if FileField or ImageField is better and non-DB file storage?
    created_by = models.CharField(max_length=250, default='internal')
    created_at = models.DateTimeField(auto_now_add=True)


class Game(models.Model):
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


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'scenario_name']
    users = ModelMultipleChoiceField(queryset=User.objects.all())


class Flag(models.Model):
    x_coordinate = models.IntegerField(default=-1)
    y_coordinate = models.IntegerField(default=-1)
    archive_x_coordinate = models.IntegerField(default=-1)
    archive_y_coordinate = models.IntegerField(default=-1)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # TODO: Decide on cascade
    order_number = models.IntegerField(default=0)
    created_by = models.CharField(max_length=250, default='internal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=250, default='internal')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.order_number}@{self.game.name}[{self.id}]'


class Bot(models.Model):
    damage = models.IntegerField(default=0)
    lives = models.IntegerField(default=3)
    x_coordinate = models.IntegerField(default=-1)
    y_coordinate = models.IntegerField(default=-1)
    archive_x_coordinate = models.IntegerField(default=-1)
    archive_y_coordinate = models.IntegerField(default=-1)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # TODO: Decide on cascade
    archive_flag = models.OneToOneField(Flag,
                                        on_delete=models.CASCADE,  # TODO: Decide on cascade
                                        null=True,
                                        blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # TODO: Decide on cascade
    order_number = models.IntegerField(default=0)
    facing_direction = models.CharField(choices=Direction.choices,
                                        max_length=5
                                        )
    created_by = models.CharField(max_length=250, default='internal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=250, default='internal')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.order_number}@{self.game.name}[{self.id}] for {self.user.name}'


class History(models.Model):
    round = models.IntegerField(default=0)
    phase = models.IntegerField(default=3)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # TODO: Decide on cascade
    snapshot = models.OneToOneField(Binary, on_delete=models.CASCADE)  # TODO: Decide on cascade
    created_by = models.CharField(max_length=250, default='internal')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.game.name}@{self.phase}/{self.round}[{self.id}]'


class Event(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # TODO: Decide on cascade
    round = models.IntegerField(default=0)
    phase = models.IntegerField(default=3)
    actor = models.ForeignKey(Bot,
                              on_delete=models.CASCADE,
                              related_name='event_actors_set')  # TODO: Decide on cascade
    victim = models.ForeignKey(Bot,
                               on_delete=models.CASCADE,
                               related_name='event_victims_set')  # TODO: Decide on cascade
    type = models.CharField(choices=EventType.choices,
                            max_length=32
                            )
    optional_text = models.CharField(max_length=250)
    created_by = models.CharField(max_length=250, default='internal')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type}@{self.game.name}@{self.phase}/{self.round}[{self.id}]'


class MovementCard(models.Model):
    round = models.IntegerField(default=0)
    phase = models.IntegerField(default=3)
    status = models.CharField(choices=CardStatus.choices,
                              max_length=10,
                              default='INITIAL'
                              )
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)  # TODO: Decide on cascade
    card_definition = models.CharField(choices=CardDefinition.choices,
                                       max_length=32
                                       )
    optional_text = models.CharField(max_length=250)
    created_by = models.CharField(max_length=250, default='internal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=250, default='internal')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.card_definition}@{self.game.name}/{self.phase}/{self.round}[{self.id}]' \
               f' for {self.bot.order_number}'
