from roborally.game.basic import BasicElement
from roborally.models import ScenarioFlag

TYPE_FLAG = 'FLAG'
KEY_SYMBOL = 'symbol'


class Flag(BasicElement):

    def __init__(self, flag: ScenarioFlag):
        super().__init__()
        self.model = flag

    def save(self):
        if self.model:
            self.model.save()

    def to_data(self):
        return {KEY_SYMBOL: str(self.model.order_number)}
