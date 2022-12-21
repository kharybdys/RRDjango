from roborally.game.basic import BasicMovableElement
from roborally.game.bot import Bot

from roborally.game.direction import to_optional_direction
from roborally.game.flag import Flag
from roborally.game.movement import Movement
from roborally_tests.mocks import FlagModelMock, BotModelMock


def to_movable(movable_element_dict: dict) -> BasicMovableElement:
    if movable_element_dict["type"] == "FLAG":
        del movable_element_dict["type"]
        movable_element_model = FlagModelMock(**movable_element_dict)
        movable = Flag(movable_element_model)
        return movable
    elif movable_element_dict["type"] == "BOT":
        del movable_element_dict["type"]
        facing_direction = to_optional_direction(movable_element_dict["facing_direction"])
        movable_element_model = BotModelMock(**dict(movable_element_dict, facing_direction=facing_direction))
        movable = Bot(movable_element_model)
        return movable
    else:
        raise ValueError(f"Unsupported movable element type: {type}")


def to_movement(movement_dict: dict, movable: BasicMovableElement) -> Movement:
    direction = to_optional_direction(movement_dict["direction"])
    return Movement(**dict(movement_dict, direction=direction, moved_object=movable))
