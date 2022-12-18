from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, ModelMultipleChoiceField

from roborally.game.direction import Direction
from roborally.game.card import CardDefinition


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
    ROTATOR_COUNTER_CLOCKWISE = 'ROTATOR_COUNTER_CLOCKWISE',
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
    element_type = models.CharField(choices=ElementTypes.choices,
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
    facing_direction = models.CharField(choices=Direction.get_choices(),
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
    card_definition = models.CharField(choices=CardDefinition.get_choices(),
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
