from roborally.models import Game


@cached
def get_game_model(game_id):
    return Game.objects.get(pk=game_id)
