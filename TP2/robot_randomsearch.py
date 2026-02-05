from robot import *
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "RandomSearch"
    robot_id = -1
    iteration = 0
    param = []
    bestParam = []
    bestScore = -1e9
    bestTrial = -1
    it_per_evaluation = 400
    max_evals = 500
    replay_iterations = 1000
    trial = 0
    replay_mode = False
    x_0 = 0
    y_0 = 0
    theta_0 = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1

        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0

        self.param = [random.randint(-1, 1) for _ in range(8)]

        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        super().reset()

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        #fin de l evaluation
        if not self.replay_mode and self.iteration % self.it_per_evaluation == 0:
            if self.iteration > 0:
                score = self.log_sum_of_translation
                print("Trial", self.trial,"// score =", score,"// params =", self.param)
                if score > self.bestScore:
                    self.bestScore = score
                    self.bestParam = self.param.copy()
                    self.bestTrial = self.trial
                    print("nouveau best trouve dans les evals", self.bestTrial,"// score =", self.bestScore)

            self.trial += 1

            #nombre total d individus atteint (500) on passe en mode replay
            if self.trial >= self.max_evals:
                self.replay_mode = True
                self.param = self.bestParam.copy()
                self.iteration = 0
                print("\nreplay de la best strategy")
                print("Best score =", self.bestScore)
                print("Best params =", self.bestParam)
                return 0, 0, True

            #nouvelle strategie aletoire
            self.param = [random.randint(-1, 1) for _ in range(8)]
            self.iteration += 1
            return 0, 0, True

        #mode replay on reset toutes les 1000
        if self.replay_mode and self.iteration % self.replay_iterations == 0:
            self.iteration += 1
            return 0, 0, True

        #controle perceptron
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )
        self.iteration += 1
        return translation, rotation, False
