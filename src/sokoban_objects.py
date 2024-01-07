from __future__ import annotations
from typing import Tuple


class GameObject:
    def __init__(self, pos: tuple) -> None:
        self._pos = pos

    @property
    def pos(self) -> Tuple[int]:
        return self._pos

    def set_pos(self, new_pos: Tuple[int]) -> None:
        self._pos = new_pos


class Wall(GameObject):
    def __init__(self, pos: tuple) -> None:
        super().__init__(pos)


class Goal(GameObject):
    def __init__(self, pos: tuple) -> None:
        super().__init__(pos)


class Character(GameObject):
    def __init__(self, pos: tuple, is_on_goal: bool) -> None:
        super().__init__(pos)
        self._is_on_goal = is_on_goal

    @property
    def is_on_goal(self) -> bool:
        return self._is_on_goal

    def set_is_on_goal_state(self, is_on_goal_state: bool) -> None:
        self._is_on_goal = is_on_goal_state


class Box(GameObject):
    def __init__(self, pos: tuple, is_on_goal: bool) -> None:
        super().__init__(pos)
        self._is_on_goal = is_on_goal

    @property
    def is_on_goal(self) -> bool:
        return self._is_on_goal

    def set_is_on_goal_state(self, is_on_goal_state: bool) -> None:
        self._is_on_goal = is_on_goal_state
