import curses
import operator
import random

from snake_py import snake, snake_move, snake_config, direction
from snake_py.controller import Controller, ControllerConfig
from snake_py.drawer import Drawer
from snake_py.game_obj import GameObj
from snake_py.position import Position


class CursesDrawer(Drawer):
    def __init__(
        self, config: snake_config.SnakeConfig, stdscr: "curses._CursesWindow"
    ) -> None:
        super().__init__(config)
        self.stdscr = stdscr

    def draw_snake(self, body: list[GameObj]) -> None:
        for cell in body:
            self.stdscr.addstr(cell.pos.y, cell.pos.x, self.config.snake_char)

    def draw_apple(self, apple: GameObj) -> None:
        self.stdscr.addstr(apple.pos.y, apple.pos.x, self.config.apple_char)


class CursesController(Controller):
    def __init__(self, config: ControllerConfig) -> None:
        super().__init__(config)

    def get_pos_after_turn(self, move: snake_move.SnakeMove) -> Position:
        if move.direction == direction.Direction.UP:
            op = operator.sub
            target = "y"
        elif move.direction == direction.Direction.LEFT:
            op = operator.sub
            target = "x"
        elif move.direction == direction.Direction.DOWN:
            op = operator.add
            target = "y"
        elif move.direction == direction.Direction.RIGHT:
            op = operator.add
            target = "x"
        else:
            raise AssertionError(f"Unknown direction: {move.direction}")

        new_pos = Position(*move.snake_pos)
        old_target = getattr(new_pos, target)
        setattr(new_pos, target, op(old_target, 1))

        return new_pos


def c_main(stdscr: "curses._CursesWindow") -> int:
    def get_random_pos():
        return Position(
            random.randrange(1, curses.COLS), random.randrange(1, curses.LINES)
        )

    def validate_position(pos: Position) -> Position:
        """Check if position in in bounds of curses window, and change if needed"""
        max_y = curses.LINES
        max_x = curses.COLS

        x = pos.x
        y = pos.y

        if x < 0:
            x = max_x - 1
        elif x > max_x - 1:
            x = 0

        if y < 0:
            y = max_y - 1
        elif y > max_y - 1:
            y = 0

        return Position(x, y)

    curses.use_default_colors()
    curses.curs_set(False)
    stdscr.nodelay(True)
    start_pos = get_random_pos()
    # center_y = curses.LINES // 2
    # center_x = curses.COLS // 2

    snake_conf = snake_config.SnakeConfig(snake_char="O", apple_char="$")
    controller_config = ControllerConfig(
        curses.KEY_UP,
        curses.KEY_RIGHT,
        curses.KEY_DOWN,
        curses.KEY_LEFT,
    )

    curses_napms = 110
    curses_napms_step_after_apple_eaten = -2

    drawer = CursesDrawer(snake_conf, stdscr)

    drct = direction.Direction.RIGHT
    controller = CursesController(controller_config)

    snake_ = snake.Snake(start_pos)
    apple = GameObj(get_random_pos())

    while True:
        curses.napms(curses_napms)
        stdscr.erase()
        stdscr.refresh()

        drawer.draw_snake(snake_.body)
        drawer.draw_apple(apple)

        if snake_.get_pos() == apple.pos:
            snake_.add_tail()
            apple.pos = get_random_pos()
            curses_napms += curses_napms_step_after_apple_eaten

        new_pos = controller.get_pos_after_turn(
            snake_move.SnakeMove(drct, snake_.get_pos())
        )
        new_pos = validate_position(new_pos)

        snake_.change_pos(new_pos)

        try:
            ch = stdscr.getch()
        except curses.error:
            pass
        else:
            if ch == 113:  # q
                break
            if ch == curses.KEY_UP:
                new_drct = direction.Direction.UP
            elif ch == curses.KEY_RIGHT:
                new_drct = direction.Direction.RIGHT
            elif ch == curses.KEY_DOWN:
                new_drct = direction.Direction.DOWN
            elif ch == curses.KEY_LEFT:
                new_drct = direction.Direction.LEFT
            else:
                continue

            if not controller.is_move_forbidden(drct, new_drct, len(snake_.body)):
                drct = new_drct

    return 0


def run():
    return curses.wrapper(c_main)
