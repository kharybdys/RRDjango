from typing import Self

from django.contrib.auth.models import User
from django.db import models

from roborally.game.card import CardDefinition
from roborally.game.direction import Direction
from roborally.game.events import EventType
from roborally.models.flag import Flag
from roborally.models.game import Game


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
        return f'{self.order_number}@{self.game.name}[{self.id}] for {self.user.username}'

    def get_cards_for(self, round, phase) -> list[CardDefinition]:
        return [CardDefinition(card)
                for card
                in self.movementcard_set.filter(round=round, phase=phase, status__in=['FINAL', 'LOCKED'])]

    def log_event(self, phase: int, event_type: EventType, other: Self = None, **kwargs):
        event = self.event_registrar_set.create(round=self.game.current_round,
                                                phase=phase,
                                                event_type=event_type,
                                                other=other,
                                                extra=kwargs)
        event.save()
