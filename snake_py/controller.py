from abc import ABC, abstractmethod
from typing import NamedTuple, TypeAlias

from snake_py import snake_move, position, direction


KeyMapping: TypeAlias = str | int


class ControllerConfig(NamedTuple):
    up_key: KeyMapping
    right_key: KeyMapping
    down_key: KeyMapping
    left_key: KeyMapping


class Controller(ABC):
    def __init__(self, config: ControllerConfig) -> None:
        self.config = config

    def is_move_forbidden(
        self,
        current_direction: direction.Direction,
        new_direction: direction.Direction,
        snake_body_count: int,
    ) -> bool:
        if snake_body_count > 1:
            if current_direction.opposite_direction() == new_direction:
                return True
        return False

    @abstractmethod
    def get_pos_after_turn(self, move: snake_move.SnakeMove) -> position.Position:
        ...
