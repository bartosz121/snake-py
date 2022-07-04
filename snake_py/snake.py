from typing import NamedTuple

from snake_py import position, game_obj


class SnakeConfig(NamedTuple):
    snake_char: str
    apple_char: str


class Snake:
    def __init__(self, start_pos: position.Position) -> None:
        head = game_obj.GameObj(start_pos)

        self.body: list[game_obj.GameObj] = [head]
        self.head = head

    def change_pos(self, new_pos: position.Position) -> None:
        head = self.body[0]
        prev_cell_pos = head.pos
        head.pos = new_pos

        for cell in self.body[1:]:
            tmp = cell.pos
            cell.pos = prev_cell_pos
            prev_cell_pos = tmp

    def add_tail(self) -> None:
        self.body.append(game_obj.GameObj(position.Position(*self.body[-1].pos)))

    def get_pos(self) -> position.Position:
        return self.body[0].pos
