import pytest

from roborally.game.direction import Direction


@pytest.mark.parametrize('start_direction, base_turns, end_direction',
                         [pytest.param(Direction.NORTH, 0, Direction.NORTH, id="north_zero_to_north"),
                          pytest.param(Direction.EAST, 0, Direction.EAST, id="east_zero_to_east"),
                          pytest.param(Direction.SOUTH, 0, Direction.SOUTH, id="south_zero_to_south"),
                          pytest.param(Direction.WEST, 0, Direction.WEST, id="west_zero_to_west"),
                          pytest.param(Direction.NORTH, 1, Direction.EAST, id="north_one_to_east"),
                          pytest.param(Direction.EAST, 1, Direction.SOUTH, id="east_one_to_south"),
                          pytest.param(Direction.SOUTH, 1, Direction.WEST, id="south_one_to_west"),
                          pytest.param(Direction.WEST, 1, Direction.NORTH, id="west_one_to_north"),
                          pytest.param(Direction.NORTH, 2, Direction.SOUTH, id="north_two_to_south"),
                          pytest.param(Direction.EAST, 2, Direction.WEST, id="east_two_to_west"),
                          pytest.param(Direction.SOUTH, 2, Direction.NORTH, id="south_two_to_north"),
                          pytest.param(Direction.WEST, 2, Direction.EAST, id="west_two_to_east"),
                          pytest.param(Direction.NORTH, 3, Direction.WEST, id="north_three_to_west"),
                          pytest.param(Direction.EAST, 3, Direction.NORTH, id="east_three_to_north"),
                          pytest.param(Direction.SOUTH, 3, Direction.EAST, id="south_three_to_east"),
                          pytest.param(Direction.WEST, 3, Direction.SOUTH, id="west_three_to_south")])
def test_direction_turn_method(start_direction: Direction, base_turns: int, end_direction: Direction):
    for turns in range(-1000, 1000, 4):
        assert end_direction == start_direction.turn(turns + base_turns)


@pytest.mark.parametrize('start_direction, end_direction, expected_turns',
                         [pytest.param(Direction.NORTH, Direction.NORTH, 0, id="north_to_north_is_zero"),
                          pytest.param(Direction.EAST, Direction.EAST, 0, id="east_to_east_is_zero"),
                          pytest.param(Direction.SOUTH, Direction.SOUTH, 0, id="south_to_south_is_zero"),
                          pytest.param(Direction.WEST, Direction.WEST, 0, id="west_to_west_is_zero"),
                          pytest.param(Direction.NORTH, Direction.EAST, 1, id="north_to_east_is_one"),
                          pytest.param(Direction.EAST, Direction.SOUTH, 1, id="east_to_south_is_one"),
                          pytest.param(Direction.SOUTH, Direction.WEST, 1, id="south_to_west_is_one"),
                          pytest.param(Direction.WEST, Direction.NORTH, 1, id="west_to_north_is_one"),
                          pytest.param(Direction.NORTH, Direction.SOUTH, 2, id="north_to_south_is_two"),
                          pytest.param(Direction.EAST, Direction.WEST, 2, id="east_to_west_is_two"),
                          pytest.param(Direction.SOUTH, Direction.NORTH, 2, id="south_to_north_is_two"),
                          pytest.param(Direction.WEST, Direction.EAST, 2, id="west_to_east_is_two"),
                          pytest.param(Direction.NORTH, Direction.WEST, 3, id="north_to_west_is_three"),
                          pytest.param(Direction.EAST, Direction.NORTH, 3, id="east_to_north_is_three"),
                          pytest.param(Direction.SOUTH, Direction.EAST, 3, id="south_to_east_is_three"),
                          pytest.param(Direction.WEST, Direction.SOUTH, 3, id="west_to_south_is_three")])
def test_direction_turns_to_method(start_direction: Direction, end_direction: Direction, expected_turns: int):
    assert start_direction.turns_to(end_direction) == expected_turns
