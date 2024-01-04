from __future__ import annotations
from typing import List
from src.state import State
from src.game_io import get_level, get_data_from_config
from src.game_io import Table


class Game:
    def __init__(self) -> None:
        self.__levs_number = get_data_from_config("levels_number")
        self.levs = range(1, self.__levs_number + 1)
        self.cur_state_num = 1
        self.levs_unlocked = set()
        self.levs_unlocked.add(self.cur_state_num)
        self.cur_state = None
        self.collector = Collector()
        self.collector.load_maps(self.load_maps_to_collector())
        self.load_level(self.cur_state_num)
        self.player = Player(self)
        self.is_game_finished = False

    @property
    def levs_number(self) -> int:
        return self.__levs_number

    def load_maps_to_collector(self) -> None:
        maps = []
        for num in self.levs:
            lev = get_level(num)
            maps.append(lev)
        return maps

    def reset_level(self) -> None:
        self.cur_state.reset()

    def unlock_level(self) -> None:
        level_to_unlock = self.cur_state_num + 1
        if level_to_unlock <= self.__levs_number:
            self.levs_unlocked.add(level_to_unlock)
        else:
            self.is_game_finished = True

    def load_level(self, num: int) -> None:
        offset = -1
        if num in self.levs_unlocked:
            self.cur_state_num = num
            level_map = self.collector.maps[self.cur_state_num + offset]
            self.cur_state = State(level_map)

    def cur_state_finished(self) -> None:
        self.unlock_level()
        self.load_level(self.cur_state_num + 1)


class Player:
    def __init__(self, game: Game) -> None:
        self.moves = {'up', 'down', 'left', 'right'}
        self.__game = game

    def move(self, move: str):
        if move in self.moves:
            self.__game.cur_state.move_object(self.__game.cur_state.character, move)
        if self.__game.cur_state.is_solved():
            self.__game.unlock_level()
            if not self.__game.is_game_finished:
                self.__game.load_level(self.__game.cur_state_num + 1)

    def reset_level(self):
        self.__game.reset_level()

    def next_level(self):
        cur_num = self.__game.cur_state_num
        self.__game.load_level(cur_num + 1)

    def prev_level(self):
        cur_num = self.__game.cur_state_num
        if cur_num != 1:
            self.__game.load_level(cur_num - 1)


class Collector:
    def __init__(self) -> None:
        self.__maps = []

    @property
    def maps(self) -> List[Table]:
        return self.__maps

    def load_maps(self, maps: List[Table]) -> None:
        for map in maps:
            self.__maps.append(map)
