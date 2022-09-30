from django.urls import path

from . import views

app_name = 'roborally'
urlpatterns = [
    path('canvas', views.CanvasView.as_view(), name='canvas'),
    path('list', views.ListGamesView.as_view(), name='list'),
    path('new', views.NewGameView.as_view(), name='new'),
    path('play/<int:pk>', views.PlayView.as_view(), name='play'),
    path('history/<int:game_id>/<int:round_number>/<int:phase>', views.HistoryView.as_view(), name='history'),
]
