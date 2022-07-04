from dataclasses import dataclass

from snake_py import position


@dataclass
class GameObj:
    pos: position.Position
