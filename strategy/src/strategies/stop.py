from strategies.base import BaseStrategy

from engine.game_state import GameState
from engine.commands import RobotCommand

from comms.udp_sender import UDPSender


class StopStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.name = "StopStrategy"
        self.description = "Stop strategy"
        self.parameters = {}

    def compute(self, state: GameState) -> list[RobotCommand]:
        return [
            RobotCommand(
                robot_id=0,
                yellow_team=True,
                wheel_left=0,
                wheel_right=0,
            )
        ]


# Ejemplo de como utilizar la estrategia.
# Esto debería recibir cuando esté el bucle principal de la app
sender = UDPSender()
state = GameState()
state.update()

strategy = StopStrategy()
commands = strategy.compute(state)
sender.send(sender.serialize(commands))
