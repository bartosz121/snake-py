from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def opposite_direction(self) -> "Direction":
        return Direction((self.value + 2) % len(Direction))
