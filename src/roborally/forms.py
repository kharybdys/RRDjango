from django.contrib.auth.models import User
from django.forms import ModelForm, ModelMultipleChoiceField, Select

from roborally.models import Game


class ScenarioNameWithPreview(Select):
    template_name = 'roborally/scenario_name_field.html'


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'scenario_name']
        widgets = {'scenario_name': ScenarioNameWithPreview()}
    users = ModelMultipleChoiceField(queryset=User.objects.all())
