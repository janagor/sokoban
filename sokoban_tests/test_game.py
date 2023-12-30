from src.game import Game
from src.game_io import get_level

lev1 = [
    ['#', '#', '#', '#', '#'],
    ['#', ' ', '*', ' ', '#'],
    ['#', '@', '$', '.', '#'],
    ['#', '#', '#', "#", '#']
]


def test_player_move(monkeypatch):
    def get_my_level(duck):
        return lev1
    game = Game()
    monkeypatch.setattr(game, "cur_state", 1)
    assert game.cur_state == 1
