from roborally.game.movable import Movable
from roborally.game.bot import Bot

from roborally.game.direction import to_optional_direction, Direction
from roborally.game.flag import Flag
from roborally.game.movement import Movement
from roborally_tests.game.events import EventChecker
from roborally_tests.mocks import Expectation, MovableModelMock


def to_movable_movement_and_expectation(event_checker: EventChecker, movable_element_dict: dict) -> (Movable, Movement, Expectation):
    if movable_element_dict["type"] == "Flag":
        cls = Flag
    elif movable_element_dict["type"] == "Bot":
        cls = Bot
    else:
        raise ValueError(f"Unsupported movable element type: {movable_element_dict['type']}")

    # remove data not used in the MovableModelMock
    expectation_dict = movable_element_dict.pop("expectation", None)
    movement_dict = movable_element_dict.pop("movement", None)
    movement_cards = movable_element_dict.pop("movement_cards", None)
    # Create the movable
    facing_direction = to_optional_direction(movable_element_dict.get("facing_direction", None))
    movable_element_model = MovableModelMock(**dict(movable_element_dict, facing_direction=facing_direction, event_checker=event_checker))
    movable = cls(movable_element_model)
    # Handle cards if applicable
    if movement_cards:
        for movement_card_dict in movement_cards:
            movable_element_model.add_card(movement_card_dict["round"], movement_card_dict["phase"], movement_card_dict["status"], movement_card_dict["card_definition"])
    # Handle movement if applicable
    if movement_dict:
        direction = to_optional_direction(movement_dict.get("direction", None))
        movement = Movement(**dict(movement_dict, direction=direction, moved_object=movable))
    else:
        movement = None
    # Handle expectation if applicable
    if expectation_dict:
        direction = to_optional_direction(expectation_dict.get("facing_direction", None))
        expectation = Expectation(**dict(expectation_dict, facing_direction=direction, movable=movable))
    else:
        expectation = None
    return movable, movement, expectation


def to_dummy_movable(x: int, y: int, direction: Direction) -> Movable:
    return Bot(MovableModelMock(x_coordinate=x, y_coordinate=y, facing_direction=direction, event_checker=None, type="Bot"))


