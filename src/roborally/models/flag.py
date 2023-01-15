from django.db import models

from roborally.models.game import Game


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
