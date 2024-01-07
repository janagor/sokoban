from __future__ import annotations
from src.sokoban_objects import Character, Box, Wall, Goal
from src.helpers import add_coords, find_object_in_type_list
from src.helpers import sok_obj_chars, dircs
from typing import Union, Tuple, List
Table = List[List[str]]


class State:
    def __init__(self, map: Table) -> None:
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

    @property
    def start_map(self):
        return self._start_map

    def init_map(self, map: Table) -> None:
        self._map = []
        self._start_map = []
        for row in map:
            self._start_map.append(row.copy())
            self._map.append(row.copy())

    def init_sokoban_objects(self) -> None:
        for ycoord, row in list(enumerate(self._map)):
            for xcoord, map_object in list(enumerate(row)):
                if map_object == sok_obj_chars['box_on_goal']:
                    self._boxes.append(Box((xcoord, ycoord), True))
                    self._goals.append(Goal((xcoord, ycoord)))
                elif map_object == sok_obj_chars['box_on_floor']:
                    self._boxes.append(Box((xcoord, ycoord), False))
                elif map_object == sok_obj_chars['char_on_floor']:
                    self.character = Character((xcoord, ycoord), False)
                elif map_object == sok_obj_chars['char_on_goal']:
                    self.character = Character((xcoord, ycoord), True)
                    self._goals.append(Goal((xcoord, ycoord)))
                elif map_object == sok_obj_chars['goal']:
                    self._goals.append(Goal((xcoord, ycoord)))
                if map_object == sok_obj_chars['wall']:
                    self._walls.append(Wall((xcoord, ycoord)))

    def update_map(self, coords: Tuple[int], new_object: str) -> bool:
        self._map[coords[1]][coords[0]] = sok_obj_chars[new_object]

    def box_move_is_legal(self, pos: Tuple[int]) -> bool:
        is_legal = True
        for map_object in self._boxes + self._walls:
            if map_object.pos == pos:
                is_legal = False
        return is_legal

    def character_move_is_legal(self, dirc: str) -> bool:
        new_pos = add_coords(self.character.pos, dircs[dirc])
        is_legal = True
        wall = self.find_wall_on_exact_pos(new_pos)
        if wall:
            is_legal = False
        if is_legal:
            box = self.find_box_on_exact_pos(new_pos)
            if box:
                behind_box = add_coords(new_pos, dircs[dirc])
                is_legal = self.box_move_is_legal(behind_box)
        return is_legal

    def move_is_legal(self, element: Union[Character, Box], dirc: str) -> bool:
        new_pos = add_coords(element.pos, dircs[dirc])
        is_legal = False
        if element == self.character:
            is_legal = self.character_move_is_legal(dirc)
        elif element in self._boxes and not is_legal:
            is_legal = self.box_move_is_legal(new_pos)
        return is_legal

    def move_object(self, element: Union[Character, Box], dirc: str) -> None:
        new_pos = add_coords(element.pos, dircs[dirc])
        if self.move_is_legal(element, dirc):
            if element.is_on_goal:
                self.update_map(element.pos, 'goal')
            else:
                self.update_map(element.pos, 'floor')

            if element == self.character:
                box = self.find_box_on_exact_pos(new_pos)
                if box:
                    self.move_object(box, dirc)

            self.update_map_next_pos(element, new_pos)
            element.set_pos(new_pos)

            if element == self.character:
                self.num_of_done_moves += 1

    def update_map_next_pos(self, element: Union[Character, Box], new_pos: Tuple[int]) -> None:
        goal_on_next_pos = self.find_goal_on_exact_pos(new_pos)
        if goal_on_next_pos:
            if element == self.character:
                self.update_map(new_pos, 'char_on_goal')
            elif element in self._boxes:
                self.update_map(new_pos, 'box_on_goal')
            element.set_is_on_goal_state(True)
        else:
            if element == self.character:
                self.update_map(new_pos, 'char_on_floor')
            elif element in self._boxes:
                self.update_map(new_pos, 'box_on_floor')
            element.set_is_on_goal_state(False)

    def find_box_on_exact_pos(self, pos: Tuple[int]) -> Box:
        return find_object_in_type_list(pos, self._boxes)

    def find_goal_on_exact_pos(self, pos: Tuple[int]) -> Goal:
        return find_object_in_type_list(pos, self._goals)

    def find_wall_on_exact_pos(self, pos: Tuple[int]) -> Wall:
        return find_object_in_type_list(pos, self._walls)

    def reset(self) -> None:
        self._boxes.clear()
        self._walls.clear()
        self._goals.clear()
        self.character = None
        self._map = []
        self.num_of_done_moves = 0
        for row in self._start_map:
            self._map.append(row.copy())

        self.init_sokoban_objects()

    def is_solved(self) -> bool:
        is_solved = True
        for box in self._boxes:
            if not box.is_on_goal:
                is_solved = False
        return is_solved
