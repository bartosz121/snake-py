from dataclasses import astuple, dataclass


@dataclass
class Position:
    x: int
    y: int

    def __iter__(self):
        return iter(astuple(self))
