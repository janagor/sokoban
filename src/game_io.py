import io
from src.state import sok_obj


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


def convert_from_file_to_map(file_handle: io.TextIOWrapper) -> list[list[str, ...], ...]:
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


def is_level_map_legal(map: list[list[str, ...], ...]) -> bool:
    map_is_legal = True
    num_of_characters = 0
    num_of_boxes = 0
    num_of_goals = 0
    for line in map:
        for element in line:
            if element == sok_obj['char_on_floor']:
                num_of_characters += 1
            elif element == sok_obj['char_on_goal']:
                num_of_characters += 1
                num_of_goals += 1
            elif element == sok_obj['goal']:
                num_of_goals += 1
            elif element == sok_obj['box_on_floor']:
                num_of_boxes += 1
            elif element == sok_obj['box_on_goal']:
                num_of_goals += 1
                num_of_boxes += 1
            if element not in sok_obj.values():
                map_is_legal = False
                raise WrongFileDataError
    if num_of_characters != 1:
        map_is_legal = False
        raise IllegalNumberOfCharactersError
    if num_of_goals != num_of_boxes:
        map_is_legal = False
        raise NumbersOfBoxesAndGoalsNotEqualError
    return map_is_legal


def get_level(level_number: int) -> list[list[str, ...], ...]:
    if not level_number:
        raise LevelNumberError
    file_name = f'{level_number}.txt'
    file_path = '../sokoban_game/levels/'
    map = None
    with open(f'{file_path}{file_name}', 'r') as f:
        map = convert_from_file_to_map(f)
    return map
