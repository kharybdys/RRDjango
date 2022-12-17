from abc import abstractmethod


class SerializationMixin:
    KEY_DIRECTION = 'direction'
    KEY_SYMBOL = 'symbol'

    @abstractmethod
    def to_data(self):
        pass
