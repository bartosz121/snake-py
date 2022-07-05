from dataclasses import dataclass, asdict

from snake_py import position, direction


@dataclass
class SnakeMove:
    direction: direction.Direction
    snake_pos: position.Position
