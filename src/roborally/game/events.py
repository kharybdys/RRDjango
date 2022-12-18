from abc import ABC


class EventException(ABC, Exception):
    pass


class MovableDiedEvent(EventException):
    pass


class WallCollisionEvent(EventException):
    pass


class BotCollisionEvent(EventException):
    pass


class MovableElementKilledEvent(EventException):
    pass
