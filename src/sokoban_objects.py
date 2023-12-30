from __future__ import annotations


class MovingObject:
    def __init__(self, pos: tuple, is_on_goal: bool):
        self._pos = pos
        self._is_on_goal = is_on_goal

    @property
    def pos(self) -> tuple(int, int):
        return self._pos

    @property
    def is_on_goal(self) -> bool:
        return self._is_on_goal

    def set_is_on_goal_state(self, is_on_goal_state: bool):
        self._is_on_goal = is_on_goal_state

    def move(self, dirc_vec: tuple):
        self._pos = tuple(x + y for x, y in zip(self.pos, dirc_vec))


class Character(MovingObject):
    def __init__(self, pos: tuple, is_on_goal: bool):
        super().__init__(pos, is_on_goal)


class Box(MovingObject):
    def __init__(self, pos: tuple, is_on_goal: bool):
        super().__init__(pos, is_on_goal)


class StationaryObject:
    def __init__(self, pos: tuple):
        self._pos = pos

    @property
    def pos(self) -> tuple(int, int):
        return self._pos


class Wall(StationaryObject):
    def __init__(self, pos: tuple):
        super().__init__(pos)


class Goal(StationaryObject):
    def __init__(self, pos: tuple):
        super().__init__(pos)
