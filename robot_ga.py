# robot_ga.py
import math
from robot import *

class Robot_player(Robot):


    def __init__(self, x_0, y_0, theta_0, name="n/a", team="A"):
        super().__init__(x_0, y_0, theta_0, name=name, team=team)
        self.param = [0,0,1,1,-1,1,1,-1]

    def reset(self):
        super().reset()

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # Même perceptron que dans GA, mais sans phase de training
        t = math.tanh(
            self.param[0]
            + self.param[1] * sensors[sensor_front_left]
            + self.param[2] * sensors[sensor_front]
            + self.param[3] * sensors[sensor_front_right]
        )
        r = math.tanh(
            self.param[4]
            + self.param[5] * sensors[sensor_front_left]
            + self.param[6] * sensors[sensor_front]
            + self.param[7] * sensors[sensor_front_right]
        )
        return t, r, False
