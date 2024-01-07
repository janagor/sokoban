from __future__ import annotations
from typing import List
from src.state import State
from src.game_io import get_level, get_data_from_config
from src.game_io import Table
from src.helpers import lev_to_load, moves


class Player:
    def __init__(self, game: Game) -> None:
        self.__game = game

    def move(self, move: str) -> None:
        if move in moves:
            self.__game.cur_state.move_object(self.__game.cur_state.character, move)
        if self.__game.cur_state.is_solved():
            self.__game.load_level(lev_to_load[2])


class Collector:
    def __init__(self) -> None:
        self.__maps = []

    @property
    def maps(self) -> List[Table]:
        return self.__maps

    def load_maps(self, maps: List[Table]) -> None:
        for map in maps:
            self.__maps.append(map)


class GameFactory:
    def __init__(self) -> None:
        starting_level = 1
        self.__levs_number = get_data_from_config("levels_number")
        self.__levs = range(1, self.__levs_number + 1)
        self.__levs_unlocked = set()
        self.__cur_lev_num = starting_level
        self.__levs_unlocked.add(self.cur_lev_num)
        self.__collector = Collector()
        self.__collector.load_maps(self.load_maps_to_collector())
        self.__is_game_finished = False

    @property
    def levs_number(self) -> int:
        return self.__levs_number

    @property
    def levs(self) -> int:
        return self.__levs

    @property
    def levs_unlocked(self) -> int:
        return self.__levs_unlocked

    @property
    def cur_lev_num(self) -> int:
        return self.__cur_lev_num

    @property
    def collector(self) -> Collector:
        return self.__collector

    @property
    def is_game_finished(self) -> bool:
        return self.__is_game_finished

    def load_maps_to_collector(self) -> List[Table]:
        maps = []
        for num in self.__levs:
            lev = get_level(num)
            maps.append(lev)
        return maps

    def unlock_level(self) -> None:
        level_to_unlock = self.cur_lev_num + 1
        if level_to_unlock <= self.__levs_number:
            self.__levs_unlocked.add(level_to_unlock)
        else:
            self.__is_game_finished = True

    def next_level(self) -> Table:
        cur_num = self.__cur_lev_num
        return self.load_level(cur_num + 1)

    def prev_level(self) -> Table:
        cur_num = self.__cur_lev_num
        if cur_num != 1:
            return self.load_level(cur_num - 1)

    def new_level(self) -> Table:
        if self.__cur_lev_num == max(self.__levs_unlocked):
            self.unlock_level()
        return self.load_level(max(self.__levs_unlocked))

    def load_level(self, num: int) -> Table:
        offset = -1
        if num in self.__levs_unlocked:
            self.__cur_lev_num = num
            level_map = self.__collector.maps[num + offset]
            return level_map


class Game:
    def __init__(self) -> None:
        self.__game_factory = GameFactory()
        self.cur_state = State(self.__game_factory.load_level(1))
        self.player = Player(self)

    @property
    def game_factory(self) -> GameFactory:
        return self.__game_factory

    def reset_level(self) -> None:
        self.cur_state.reset()

    def load_level(self, load_type: str) -> None:
        if load_type == lev_to_load[0]:
            level = self.__game_factory.prev_level()
            if level:
                self.cur_state = State(level)
        elif load_type == lev_to_load[1]:
            level = self.__game_factory.next_level()
            if level:
                self.cur_state = State(level)
        elif load_type == lev_to_load[2]:
            self.cur_state = State(self.__game_factory.new_level())
