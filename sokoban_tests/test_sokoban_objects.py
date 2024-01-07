from src.sokoban_objects import GameObject, Character, Box
from src.sokoban_objects import Wall, Goal


def test_create_game_object():
    game_object = GameObject((2, 2))
    assert game_object.pos == (2, 2)


def test_create_character():
    character = Character((2, 2), False)
    assert not character.is_on_goal
    assert character.pos == (2, 2)


def test_create_box():
    box = Box((2, 2), False)
    assert not box.is_on_goal
    assert box.pos == (2, 2)


def test_create_wall():
    wall = Wall((2, 2))
    assert wall.pos == (2, 2)


def test_create_goal():
    goal = Goal((2, 2))
    assert goal.pos == (2, 2)
