from os import path

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from roborally.board.data.data_django import DjangoScenarioDataProvider
from roborally.board.data.data_json import JSONScenarioDataProvider
from roborally.models import Game, History, Bot
from roborally.forms import GameForm
from roborally.board.scenario import Scenario


# Test canvas
class TestScenarioView(generic.TemplateView):
    template_name = 'roborally/test_scenario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with open(path.join(path.split(__file__)[0],  "../../tests/roborally_tests/board/test_scenario.json"), 'r') as f:
            scenario_data_provider = JSONScenarioDataProvider(f.read())
        board_data = Scenario(scenario_data_provider, True).to_data()
        context['board'] = board_data
        return context


class ScenarioCanvasPartialView(generic.TemplateView):
    template_name = 'roborally/canvas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scenario_data_provider = DjangoScenarioDataProvider(kwargs["scenario_name"].upper())
        board_data = Scenario(scenario_data_provider, True).to_data()
        context['board'] = board_data
        return context


# list games
@method_decorator(login_required, name='dispatch')
class ListGamesView(generic.ListView):
    template_name = 'roborally/list.html'
    context_object_name = 'game_list'

    def get_queryset(self):
        return Game.objects.filter(bot__user=self.request.user)


@method_decorator(login_required, name='dispatch')
class NewGameView(generic.CreateView):
    template_name = 'roborally/new.html'
    form_class = GameForm
    context_object_name = 'game_form'

    def form_valid(self, form):
        form.instance.created_by = self.request.user.id
        response = super().form_valid(form)
        # add bot for the current user
        bot = Bot(game=self.object,
                  user=self.request.user,
                  created_by=self.request.user.id,
                  updated_by=self.request.user.id)
        bot.save()
        # add bots for the chosen users
        for player in form.cleaned_data['users']:
            bot = Bot(game=self.object,
                      user=player,
                      created_by=self.request.user.id,
                      updated_by=self.request.user.id)
            bot.save()
        return response

    def get_success_url(self):
        return reverse('roborally:play', kwargs={'pk': self.object.pk})


# see current game state
@method_decorator(login_required, name='dispatch')
class PlayView(generic.DetailView):
    model = Game
    template_name = 'roborally/play.html'


# popup for history?
@method_decorator(login_required, name='dispatch')
class HistoryView(generic.DetailView):
    context_object_name = 'history'
    model = History
    template_name = 'roborally/history.html'

    def get_queryset(self):
        return History.objects.get(game_id=self.kwargs['game_id'],
                                   round=self.kwargs['round_number'],
                                   phase=self.kwargs['phase'])
