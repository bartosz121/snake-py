from abc import ABC, abstractmethod
from typing import NamedTuple, TypeAlias
from enum import Enum, auto

from snake_py import position


class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


KeyMapping: TypeAlias = str | int


class ControllerConfig(NamedTuple):
    up_key: KeyMapping
    right_key: KeyMapping
    down_key: KeyMapping
    left_key: KeyMapping


class Controller(ABC):
    def __init__(self, config: ControllerConfig) -> None:
        self.config = config

    @abstractmethod
    def get_pos_after_turn(
        self, direction: Direction, current_pos: position.Position
    ) -> position.Position:
        ...
