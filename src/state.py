from __future__ import annotations
from src.sokoban_objects import Character, Box, Wall, Goal

sok_obj = {
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


class State:
    def __init__(self, map):
        self.init_map(map)

        self._boxes = []
        self._walls = []
        self._goals = []
        self.character = None
        self.init_sokoban_objects()
        self.num_of_done_moves = 0

    @property
    def map(self):
        return self._map

    def init_map(self, map):
        self._map = []
        self._start_map = []
        for row in map:
            self._start_map.append(row.copy())
            self._map.append(row.copy())

    def init_sokoban_objects(self):
        for ycoord, row in list(enumerate(self._map)):
            for xcoord, map_object in list(enumerate(row)):
                if map_object == sok_obj['box_on_goal']:
                    self._boxes.append(Box((xcoord, ycoord), True))
                    self._goals.append(Goal((xcoord, ycoord)))
                elif map_object == sok_obj['box_on_floor']:
                    self._boxes.append(Box((xcoord, ycoord), False))
                elif map_object == sok_obj['char_on_floor']:
                    self.character = Character((xcoord, ycoord), False)
                elif map_object == sok_obj['char_on_goal']:
                    self.character = Character((xcoord, ycoord), True)
                    self._goals.append(Goal((xcoord, ycoord)))
                elif map_object == sok_obj['goal']:
                    self._goals.append(Goal((xcoord, ycoord)))
                if map_object == sok_obj['wall']:
                    self._walls.append(Wall((xcoord, ycoord)))

    def update_map(self, coords: tuple, new_object: sok_obj.keys()):
        self._map[coords[1]][coords[0]] = sok_obj[new_object]

    def add_coords(self, coords1, coords2):
        return tuple(x + y for x, y in zip(coords1, coords2))

    def box_move_is_legal(self, pos):
        is_legal = True
        for map_object in self._boxes + self._walls:
            if map_object.pos == pos:
                is_legal = False
        return is_legal

    def move_box(self, box: Box, dirc: dircs.keys()):
        new_pos = self.add_coords(box.pos, dircs[dirc])
        if self.box_move_is_legal(new_pos):
            if box.is_on_goal:
                self.update_map(box.pos, 'goal')
            else:
                self.update_map(box.pos, 'floor')

            goal_on_new_pos = False
            for goal in self._goals:
                if goal.pos == new_pos:
                    goal_on_new_pos = True
            if goal_on_new_pos:
                self.update_map(new_pos, 'box_on_goal')
                box.set_is_on_goal_state(True)
            else:
                self.update_map(new_pos, 'box_on_floor')
                box.set_is_on_goal_state(False)

            box.move(dircs[dirc])

    def character_move_is_legal(self, dirc: dircs.keys()):
        new_pos = self.add_coords(self.character.pos, dircs[dirc])
        is_legal = True
        for wall in self._walls:
            if wall.pos == new_pos:
                is_legal = False
        if is_legal:
            for box in self._boxes:
                if box.pos == new_pos:
                    behind_box = self.add_coords(new_pos, dircs[dirc])
                    is_legal = self.box_move_is_legal(behind_box)
        return is_legal

    def move_character(self, dirc):
        new_pos = self.add_coords(self.character.pos, dircs[dirc])
        if self.character_move_is_legal(dirc):
            if self.character.is_on_goal:
                self.update_map(self.character.pos, 'goal')
            else:
                self.update_map(self.character.pos, 'floor')

            for box in self._boxes:
                if box.pos == new_pos:
                    self.move_box(box, dirc)

            goal_on_next_pos = False
            for goal in self._goals:
                if goal.pos == new_pos:
                    goal_on_next_pos = True
            if goal_on_next_pos:
                self.update_map(new_pos, 'char_on_goal')
                self.character.set_is_on_goal_state(True)
            else:
                self.update_map(new_pos, 'char_on_floor')
                self.character.set_is_on_goal_state(False)

            self.character.move(dircs[dirc])
            self.num_of_done_moves += 1

    def is_level_solved(self):
        is_solved = True
        for box in self._boxes:
            if not box.is_on_goal:
                is_solved = False
        return is_solved

    def find_object_in_type_list(self, pos, type_list):
        chosen_object = None
        for game_object in type_list:
            if game_object.pos == pos:
                chosen_object = game_object
        return chosen_object

    def find_box_on_exact_pos(self, pos):
        return self.find_object_in_type_list(pos, self._boxes)

    def find_goal_on_exact_pos(self, pos):
        return self.find_object_in_type_list(pos, self._goals)

    def reset(self):
        self._boxes.clear()
        self._walls.clear()
        self._goals.clear()
        self.character = None
        self._map = []
        self.num_of_done_moves = 0
        for row in self._start_map:
            self._map.append(row.copy())

        self.init_sokoban_objects()

    def is_solved(self):
        is_solved = True
        for box in self._boxes:
            if not box.is_on_goal:
                is_solved = False
        return is_solved
