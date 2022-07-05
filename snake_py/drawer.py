from abc import ABC, abstractmethod
from snake_py import game_obj, snake_config


class Drawer(ABC):
    def __init__(self, config: snake_config.SnakeConfig) -> None:
        self.config = config

    @abstractmethod
    def draw_snake(self, body: list[game_obj.GameObj]):
        ...

    @abstractmethod
    def draw_apple(self, apple: game_obj.GameObj):
        ...
