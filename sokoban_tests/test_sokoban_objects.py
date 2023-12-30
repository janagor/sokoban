from src.sokoban_objects import MovingObject, Character, Box
from src.sokoban_objects import StationaryObject, Wall, Goal


def test_create_moving_object():
    moving_object = MovingObject((2, 2), False)
    assert not moving_object.is_on_goal
    assert moving_object.pos == (2, 2)


def test_create_character():
    character = Character((2, 2), False)
    assert not character.is_on_goal
    assert character.pos == (2, 2)


def test_create_box():
    box = Box((2, 2), False)
    assert not box.is_on_goal
    assert box.pos == (2, 2)


def test_create_stationary_object():
    stationary_object = StationaryObject((2, 2))
    assert stationary_object.pos == (2, 2)


def test_create_wall():
    wall = Wall((2, 2))
    assert wall.pos == (2, 2)


def test_create_goal():
    goal = Goal((2, 2))
    assert goal.pos == (2, 2)
