from django.db import models

from roborally.game.card import CardDefinition
from roborally.models.bot import Bot


class CardStatus(models.TextChoices):
    INITIAL = 'INITIAL'
    FINAL = 'FINAL'
    LOCKED = 'LOCKED'
    FLYWHEEL = 'FLYWHEEL'


class MovementCard(models.Model):
    round = models.IntegerField(default=0)
    phase = models.IntegerField(default=1)
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
        return f'{self.card_definition}@{self.bot.game.name}/{self.phase}/{self.round}[{self.id}]' \
               f' for {self.bot.order_number}'
