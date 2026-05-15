from comms.udp_receiver import UDPReceiver


class GameState:
    def __init__(self):
        self.frame = None
        self.field = None
        self.goals_blue = None
        self.goals_yellow = None

    def update(self):
        self.frame, self.field, self.goals_blue, self.goals_yellow = (
            UDPReceiver().deserialize(UDPReceiver().receive())
        )

    def get_ball(self):
        return (
            self.frame.ball.x,
            self.frame.ball.y,
            self.frame.ball.vx,
            self.frame.ball.vy,
        )

    def get_yellow_robots(self):
        return self.frame.robots_yellow

    def get_blue_robots(self):
        return self.frame.robots_blue

    def get_game_score(self):
        return self.goals_yellow, self.goals_blue

    def get_field_dimensions(self):
        return (
            self.field.width,
            self.field.length,
            self.field.goal_width,
            self.field.goal_depth,
        )
