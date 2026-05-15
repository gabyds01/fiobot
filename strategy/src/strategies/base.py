from abc import ABC, abstractmethod

from engine.game_state import GameState

from engine.commands import RobotCommand


class BaseStrategy(ABC):
    def __init__(self):
        self.name = "BaseStrategy"
        self.description = "Base strategy for testing"
        self.parameters = {}

    @abstractmethod
    def compute(self, state: GameState) -> list[RobotCommand]:
        pass

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass
