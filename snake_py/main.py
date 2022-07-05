import curses
import operator
import random

from snake_py import snake
from snake_py.controller import Controller, ControllerConfig, Direction
from snake_py.drawer import Drawer
from snake_py.game_obj import GameObj
from snake_py.position import Position


class CursesDrawer(Drawer):
    def __init__(
        self, config: snake.SnakeConfig, stdscr: "curses._CursesWindow"
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

    def get_pos_after_turn(
        self, direction: Direction, current_pos: Position
    ) -> Position:
        if direction == Direction.UP:
            op = operator.sub
            target = "y"
        elif direction == Direction.LEFT:
            op = operator.sub
            target = "x"
        elif direction == Direction.DOWN:
            op = operator.add
            target = "y"
        elif direction == Direction.RIGHT:
            op = operator.add
            target = "x"
        else:
            raise AssertionError(f"Unknown direction: {direction}")

        new_pos = Position(*current_pos)
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

    snake_config = snake.SnakeConfig(snake_char="O", apple_char="$")
    controller_config = ControllerConfig(
        curses.KEY_UP,
        curses.KEY_RIGHT,
        curses.KEY_DOWN,
        curses.KEY_LEFT,
    )

    curses_napms = 110
    curses_napms_step_after_apple_eaten = -2

    drawer = CursesDrawer(snake_config, stdscr)
    controller = CursesController(controller_config)
    snake_ = snake.Snake(start_pos)
    apple = GameObj(get_random_pos())

    direction = Direction.RIGHT
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

        new_pos = controller.get_pos_after_turn(direction, snake_.get_pos())
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
                direction = Direction.UP
            elif ch == curses.KEY_RIGHT:
                direction = Direction.RIGHT
            elif ch == curses.KEY_DOWN:
                direction = Direction.DOWN
            elif ch == curses.KEY_LEFT:
                direction = Direction.LEFT
            else:
                continue

    return 0


def run():
    return curses.wrapper(c_main)
