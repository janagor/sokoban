from __future__ import annotations
from src.state import State
from src.game_io import get_level


class Game:
    def __init__(self):
        self.__num_of_levs = 2
        self.levs = range(1, self.__num_of_levs + 1)
        self.levs_unlocked = {1}
        self.cur_state_num = 1
        self.cur_state = None
        self.database = Database()
        self.database.load_maps(self.load_maps_to_database())
        self.load_level(self.cur_state_num)
        self.player = Player(self)
        self.is_game_finished = False

    @property
    def num_of_levs(self):
        return self.__num_of_levs

    def load_maps_to_database(self):
        maps = []
        for num in self.levs:
            lev = get_level(num)
            maps.append(lev)
        return maps

    def reset_level(self):
        self.cur_state.reset()

    def unlock_level(self):
        level_to_unlock = self.cur_state_num + 1
        if level_to_unlock <= self.__num_of_levs:
            self.levs_unlocked.add(level_to_unlock)
        else:
            self.is_game_finished = True

    def load_level(self, num):
        offset = -1
        self.cur_state_num = num
        if self.cur_state_num in self.levs_unlocked:
            level_map = self.database.maps[self.cur_state_num + offset]
            self.cur_state = State(level_map)

    def cur_state_finished(self):
        self.unlock_level()
        self.load_level(self.cur_state_num + 1)


class Player:
    def __init__(self, game):
        self.moves = {'up', 'down', 'left', 'right'}
        self.__game = game

    def move(self, move):
        if move in self.moves:
            self.__game.cur_state.move_character(move)
        if self.__game.cur_state.is_level_solved():
            self.__game.unlock_level()
            if not self.__game.is_game_finished:
                self.__game.load_level(self.__game.cur_state_num + 1)

    def reset_level(self):
        self.__game.reset_level()


class Database:
    def __init__(self):
        self.__maps = []

    @property
    def maps(self):
        return self.__maps

    def load_maps(self, maps):
        for map in maps:
            self.__maps.append(map)

