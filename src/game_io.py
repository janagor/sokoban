from __future__ import annotations
import json
from src.state import sok_obj_chars
from typing import IO, Union, List
Table = List[List[str]]

path = './src/config.json'


class WrongFileDataError(Exception):
    pass


class LevelNumberError(Exception):
    pass


class IllegalNumberOfCharactersError(Exception):
    pass


class NumbersOfBoxesAndGoalsNotEqualError(Exception):
    pass


class MelfomedMapError(Exception):
    pass


def convert_from_file_to_map(file_handle: IO) -> Table:
    map = []
    for lines in file_handle:
        pos_lines = lines.rstrip()
        if len(pos_lines) == 0:
            continue
        map.append(list(pos_lines))
    if is_level_map_legal(map):
        return map
    else:
        raise MelfomedMapError


def is_level_map_legal(map: Table) -> bool:
    map_is_legal = True
    num_of_characters = 0
    num_of_boxes = 0
    num_of_goals = 0
    for line in map:
        for element in line:
            if element == sok_obj_chars['char_on_floor']:
                num_of_characters += 1
            elif element == sok_obj_chars['char_on_goal']:
                num_of_characters += 1
                num_of_goals += 1
            elif element == sok_obj_chars['goal']:
                num_of_goals += 1
            elif element == sok_obj_chars['box_on_floor']:
                num_of_boxes += 1
            elif element == sok_obj_chars['box_on_goal']:
                num_of_goals += 1
                num_of_boxes += 1
            if element not in sok_obj_chars.values():
                map_is_legal = False
                raise WrongFileDataError
    if num_of_characters != 1:
        map_is_legal = False
        raise IllegalNumberOfCharactersError
    if num_of_goals != num_of_boxes:
        map_is_legal = False
        raise NumbersOfBoxesAndGoalsNotEqualError
    return map_is_legal


def get_level(level_number: int) -> Table:
    if not level_number:
        raise LevelNumberError
    file_name = f'{level_number}.txt'
    file_path = get_data_from_config("path_to_levels")
    map = None
    with open(f'{file_path}{file_name}', 'r') as f:
        map = convert_from_file_to_map(f)
    return map


def get_data_from_config(param: str) -> Union[int, str]:
    value = None
    with open(path, 'r') as file_handle:
        config_data = json.load(file_handle)
        value = config_data[param]
    return value
