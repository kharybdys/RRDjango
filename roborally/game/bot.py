from roborally.game.basic import BasicElement


class Bot(BasicElement):
    INITIAL_HEALTH = 10

    def __init__(self, bot):
        super().__init__()
        self.model = bot
        self.damage = 0

    def save(self):
        if self.model:
            self.model.save()

    def paint(self):
        pass
