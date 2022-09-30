from django.contrib import admin

# Register your models here.

from .models import Scenario, ScenarioFlag, BoardElement

admin.site.register(Scenario)
admin.site.register(ScenarioFlag)
admin.site.register(BoardElement)
