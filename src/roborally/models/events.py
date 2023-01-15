from django.db import models

from roborally.game.events import EventType
from roborally.models.bot import Bot


class Event(models.Model):
    round = models.IntegerField(default=0)
    phase = models.IntegerField(default=1)
    registrar = models.ForeignKey(Bot,
                                  on_delete=models.CASCADE,
                                  related_name='event_registrar_set')  # TODO: Decide on cascade
    other = models.ForeignKey(Bot,
                              on_delete=models.CASCADE,
                              related_name='event_other_set')  # TODO: Decide on cascade
    type = models.CharField(choices=EventType.get_choices(),
                            max_length=32
                            )
    extra = models.CharField(max_length=2500)
    created_by = models.CharField(max_length=250, default='internal')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type}@{self.registrar.game.name}@{self.phase}/{self.round}[{self.id}]'
