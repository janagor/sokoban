from src.state import State
import pytest

lev1 = [
    ['#', '#', '#', '#', '#'],
    ['#', ' ', '*', ' ', '#'],
    ['#', '@', '$', '.', '#'],
    ['#', '#', '#', "#", '#']
]

lev2 = [
    ['#', '#', '#', '#', '#'],
    ['#', ' ', '*', ' ', '#'],
    ['#', '.', '@', '$', '#'],
    ['#', '#', '#', "#", '#']
]


def test_init_state():
    state = State(lev1)
    assert len(state._boxes) == 2
    assert state.character.pos == (1, 2)
    assert len(state._goals) == 2
    assert len(state._walls) == 14


def test_update_map():
    state = State(lev1)
    state.update_map((0, 0), 'floor')
    assert state._map[0][0] == ' '


def test_move_box():
    state = State(lev1)
    box_pos = (2, 2)
    direction = 'right'
    box = state.find_box_on_exact_pos(box_pos)
    state.move_object(box, direction)
    assert box.pos == (3, 2)


def test_move_box_illegal_into_wall():
    state = State(lev1)
    start_pos = (2, 2)
    dirc = 'down'
    box = state.find_box_on_exact_pos(start_pos)
    state.move_object(box, dirc)
    assert box.pos == start_pos


def test_move_box_illegal_into_other_box():
    state = State(lev1)
    start_pos = (2, 2)
    dirc = 'up'
    box = state.find_box_on_exact_pos(start_pos)
    state.move_object(box, dirc)
    assert box.pos == start_pos


def test_move_box_change_in_map():
    state = State(lev1)
    box_pos = (2, 2)
    dirc = 'right'
    box = state.find_box_on_exact_pos(box_pos)
    state.move_object(box, dirc)
    assert state._map[2][2] == ' '
    assert state._map[2][3] == '*'


def test_illegal_move_no_change_in_map():
    state = State(lev1)
    start_pos = (2, 2)
    dirc = 'down'
    box = state.find_box_on_exact_pos(start_pos)
    state.move_object(box, dirc)
    assert state._map[2][2] == '$'
    assert state._map[3][2] == '#'


def test_character_move_is_legal_onto_floor():
    state = State(lev1)
    assert state.character_move_is_legal('up')


def test_character_move_is_legal_box_can_move():
    state = State(lev1)
    assert state.character_move_is_legal('right')


def test_character_move_is_illegal_wall():
    state = State(lev1)
    assert not state.character_move_is_legal('left')


def test_character_move_is_illegal_box_cannot_move():
    state = State(lev2)
    state.init_sokoban_objects()
    assert not state.character_move_is_legal('right')


def test_move_character_onto_floor():
    state = State(lev1)
    dirc = 'up'
    state.move_object(state.character, dirc)
    assert state.character._pos == (1, 1)


def test_move_character_into_box_that_can_move():
    state = State(lev1)
    dirc = 'right'
    state.move_object(state.character, dirc)
    assert state.character._pos == (2, 2)
    assert state._map[2][1] == ' '
    assert state._map[2][2] == '@'
    assert state._map[2][3] == '*'


def test_move_character_into_wall():
    state = State(lev1)
    dirc = 'left'
    state.move_object(state.character, dirc)
    assert state.character._pos == (1, 2)
    assert state._map[2][1] == '@'
    assert state._map[2][0] == '#'


def test_move_character_into_box_that_cannot_move():
    state = State(lev2)
    dirc = 'right'
    state.move_object(state.character, dirc)
    assert state.character._pos == (2, 2)
    assert state._map[2][2] == '@'
    assert state._map[2][3] == '$'
    assert state._map[2][4] == '#'


def test_reset_state():
    state = State(lev1)
    dirc = 'right'
    state.move_object(state.character, dirc)
    assert state._map is not state._start_map
    state.reset()
    assert state._map == state._start_map


def test_level_is_not_solved():
    state = State(lev1)
    assert not state.is_solved()


def test_level_is_solved():
    state = State(lev1)
    dirc = 'right'
    state.move_object(state.character, dirc)
    assert state.is_solved()
