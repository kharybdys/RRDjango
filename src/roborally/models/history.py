from django.db import models

from roborally.models.game import Game


class History(models.Model):
    round = models.IntegerField(default=0)
    phase = models.IntegerField(default=1)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # TODO: Decide on cascade
    snapshot_data = models.JSONField
    created_by = models.CharField(max_length=250, default='internal')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.game.name}@{self.phase}/{self.round}[{self.id}]'
