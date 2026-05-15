from dataclasses import dataclass


@dataclass
class RobotCommand:
    robot_id: int
    yellow_team: bool
    wheel_left: float
    wheel_right: float
