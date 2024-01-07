from src.game_io import convert_from_file_to_map, get_level
from src.game_io import WrongFileDataError
from src.game_io import LevelNumberError
from src.game_io import IllegalNumberOfCharactersError
from src.game_io import NumbersOfBoxesAndGoalsNotEqualError
from src.game_io import NoLevelError
import pytest
from io import StringIO


def test_convert_from_file_to_map():
    data = "#.\n$@ \n"
    path = StringIO(data)
    map = convert_from_file_to_map(path)
    assert len(map) == 2
    assert map[0][0] == '#'
    assert map[0][1] == '.'
    assert map[1][0] == '$'
    assert map[1][1] == '@'
    assert isinstance(map, list)


def test_no_file():
    with pytest.raises(LevelNumberError):
        get_level('')


def test_incorrect_data_in_file():
    data = "##  +#1"
    path = StringIO(data)
    with pytest.raises(WrongFileDataError):
        convert_from_file_to_map(path)


def test_incorrect_number_of_characters():
    data = "##\n$ \n  #@+"
    path = StringIO(data)
    with pytest.raises(IllegalNumberOfCharactersError):
        convert_from_file_to_map(path)


def test_numbers_of_goals_and_boxes_not_equal():
    data = "####\n# *#\n#@$#\n####"
    path = StringIO(data)
    with pytest.raises(NumbersOfBoxesAndGoalsNotEqualError):
        convert_from_file_to_map(path)


def test_level_number_does_not_exist():
    with pytest.raises(NoLevelError):
        get_level(123)
