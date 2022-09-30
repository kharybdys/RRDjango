from roborally.game.basic import BasicElement

TYPE_FLAG = 'FLAG'


class Flag(BasicElement):

    def __init__(self, flag):
        super().__init__()
        self.model = flag

    def save(self):
        if self.model:
            self.model.save()

    def paint(self):
        pass
