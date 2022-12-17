from django.contrib import admin

# Register your models here.

from .models import ScenarioBoard, ScenarioFlag, BoardElement

admin.site.register(ScenarioBoard)
admin.site.register(ScenarioFlag)
admin.site.register(BoardElement)
