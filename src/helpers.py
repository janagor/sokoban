from typing import Tuple, Union, List
from src.sokoban_objects import Box, Wall, Goal

sok_obj_chars = {
    'box_on_floor': '$',
    'box_on_goal': '*',
    'char_on_floor': '@',
    'char_on_goal': '+',
    'floor': ' ',
    'wall': '#',
    'goal': '.',
}

dircs = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}


def add_coords(coords1: Tuple[int], coords2: Tuple[int]) -> Tuple[int]:
    return tuple(x + y for x, y in zip(coords1, coords2))


def find_object_in_type_list(pos, type_list: List[Union[Box, Wall, Goal]]) -> Union[Box, Wall, Goal]:
    chosen_object = None
    for game_object in type_list:
        if game_object.pos == pos:
            chosen_object = game_object
    return chosen_object
