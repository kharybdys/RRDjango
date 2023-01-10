from django.urls import path

from . import views

app_name = 'roborally'
urlpatterns = [
    path('test_scenario', views.TestScenarioView.as_view(), name='test_scenario'),
    path('scenario/<str:scenario_name>', views.ScenarioCanvasPartialView.as_view(), name='scenario_details'),
    path('list', views.ListGamesView.as_view(), name='list'),
    path('new', views.NewGameView.as_view(), name='new'),
    path('play/<int:pk>', views.PlayView.as_view(), name='play'),
    path('history/<int:game_id>/<int:round_number>/<int:phase>', views.HistoryView.as_view(), name='history'),
]
