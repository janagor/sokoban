from src.game import Game, Collector, GameFactory
from src.game_io import Table
import src.game
from typing import Any, List
lev1 = [
    ['#', '#', '#', '#', '#'],
    ['#', ' ', '*', ' ', '#'],
    ['#', '@', '$', '.', '#'],
    ['#', '#', '#', "#", '#']
]
lev2 = [
    ['#', '#', '#', '#', '#', '#'],
    ['#', '@', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', '$', '.', '#'],
    ['#', ' ', '.', '$', ' ', '#'],
    ['#', '#', '#', '#', '#', '#']
]
lev3 = [
    [' ', ' ', '#', '#', '#'],
    [' ', ' ', '#', '.', '#'],
    [' ', ' ', '#', ' ', '#', '#', '#', '#'],
    ['#', '#', '#', '$', ' ', '$', '.', '#'],
    ['#', '.', ' ', '$', '@', '#', '#', '#'],
    ['#', '#', '#', '#', '$', '#'],
    [' ', ' ', ' ', '#', '.', '#'],
    [' ', ' ', ' ', '#', '#', '#']
]
levels = [lev1, lev2, lev3]


def mock_get_level(lev_num: int) -> Table:
    return levels[lev_num - 1]


def mock_load_level(self, lev_num: int) -> Table:
    return levels[lev_num - 1]


def mock_get_data_from_config(param: Any) -> int:
    return len(levels)


def mock_load_maps_to_collector(param: Any) -> List[Table]:
    return levels


def test_player_move(monkeypatch):
    game = Game()
    monkeypatch.setattr(game, "cur_state", mock_get_level(1))
    assert game.cur_state == lev1


def test_collector():
    collector = Collector()
    collector.load_maps(levels)
    assert collector.maps[0] == lev1
    assert collector.maps[1] == lev2
    assert collector.maps[2] == lev3


def test_game_factory_init(monkeypatch):
    monkeypatch.setattr(src.game, 'get_data_from_config', mock_get_data_from_config)
    monkeypatch.setattr(GameFactory, 'load_maps_to_collector', mock_load_maps_to_collector)
    game_factory = GameFactory()
    assert game_factory.levs_number == 3
    assert list(game_factory.levs) == [1, 2, 3]
    assert game_factory.levs_unlocked == {1}
    assert game_factory.collector.maps[0] == lev1
    assert game_factory.collector.maps[1] == lev2
    assert game_factory.collector.maps[2] == lev3
    assert not game_factory.is_game_finished


def test_game_factory_unlock_level(monkeypatch):
    monkeypatch.setattr(src.game, 'get_data_from_config', mock_get_data_from_config)
    monkeypatch.setattr(GameFactory, 'load_maps_to_collector', mock_load_maps_to_collector)
    game_factory = GameFactory()
    game_factory.unlock_level()
    assert game_factory.levs_unlocked == {1, 2}
    assert game_factory.cur_lev_num == 1


def test_game_factory_load_level(monkeypatch):
    monkeypatch.setattr(src.game, 'get_data_from_config', mock_get_data_from_config)
    monkeypatch.setattr(GameFactory, 'load_maps_to_collector', mock_load_maps_to_collector)
    game_factory = GameFactory()
    game_factory.unlock_level()
    game_factory.load_level(2)
    assert game_factory.cur_lev_num == 2


def test_game_factory_next_level_when_unlocked(monkeypatch):
    monkeypatch.setattr(src.game, 'get_data_from_config', mock_get_data_from_config)
    monkeypatch.setattr(GameFactory, 'load_maps_to_collector', mock_load_maps_to_collector)
    game_factory = GameFactory()
    game_factory.unlock_level()
    game_factory.next_level()
    assert game_factory.cur_lev_num == 2


def test_game_factory_next_level_when_not_unlocked(monkeypatch):
    monkeypatch.setattr(src.game, 'get_data_from_config', mock_get_data_from_config)
    monkeypatch.setattr(GameFactory, 'load_maps_to_collector', mock_load_maps_to_collector)
    game_factory = GameFactory()
    game_factory.next_level()
    assert game_factory.cur_lev_num == 1


def test_game_factory_prev_level_when_cur_is_1(monkeypatch):
    monkeypatch.setattr(src.game, 'get_data_from_config', mock_get_data_from_config)
    monkeypatch.setattr(GameFactory, 'load_maps_to_collector', mock_load_maps_to_collector)
    game_factory = GameFactory()
    game_factory.prev_level()
    assert game_factory.cur_lev_num == 1


def test_game_factory_prev_level_when_cur_is_more_then_1(monkeypatch):
    monkeypatch.setattr(src.game, 'get_data_from_config', mock_get_data_from_config)
    monkeypatch.setattr(GameFactory, 'load_maps_to_collector', mock_load_maps_to_collector)
    game_factory = GameFactory()
    game_factory.unlock_level()
    game_factory.next_level()
    assert game_factory.cur_lev_num == 2
    game_factory.prev_level()
    assert game_factory.cur_lev_num == 1


def test_game_factory_new_level(monkeypatch):
    monkeypatch.setattr(src.game, 'get_data_from_config', mock_get_data_from_config)
    monkeypatch.setattr(GameFactory, 'load_maps_to_collector', mock_load_maps_to_collector)
    game_factory = GameFactory()
    game_factory.new_level()
    assert game_factory.cur_lev_num == 2


def test_game_init(monkeypatch):
    monkeypatch.setattr(src.game, 'get_data_from_config', mock_get_data_from_config)
    monkeypatch.setattr(GameFactory, 'load_maps_to_collector', mock_load_maps_to_collector)
    game = Game()
    assert game.cur_state.map == lev1
    assert game.cur_state.start_map == lev1


def test_game_load_new_level(monkeypatch):
    monkeypatch.setattr(src.game, 'get_data_from_config', mock_get_data_from_config)
    monkeypatch.setattr(GameFactory, 'load_maps_to_collector', mock_load_maps_to_collector)
    game = Game()
    assert game.cur_state.map == lev1
    game.load_level('new')
    assert game.cur_state.map == lev2
    game.load_level('new')
    assert game.cur_state.map == lev3


def test_game_load_prev_level(monkeypatch):
    monkeypatch.setattr(src.game, 'get_data_from_config', mock_get_data_from_config)
    monkeypatch.setattr(GameFactory, 'load_maps_to_collector', mock_load_maps_to_collector)
    game = Game()
    game.load_level('new')
    game.load_level('prev')
    assert game.cur_state.map == lev1


def test_game_load_next_level(monkeypatch):
    monkeypatch.setattr(src.game, 'get_data_from_config', mock_get_data_from_config)
    monkeypatch.setattr(GameFactory, 'load_maps_to_collector', mock_load_maps_to_collector)
    game = Game()
    game.load_level('new')
    game.load_level('prev')
    game.load_level('next')
    assert game.cur_state.map == lev2


def test_game_load_reset_level(monkeypatch):
    monkeypatch.setattr(src.game, 'get_data_from_config', mock_get_data_from_config)
    monkeypatch.setattr(GameFactory, 'load_maps_to_collector', mock_load_maps_to_collector)
    game = Game()
    assert game.cur_state.map == lev1
    game.cur_state.move_object(game.cur_state.character, 'up')
    assert game.cur_state.map != lev1
    game.reset_level()
    assert game.cur_state.map == lev1
