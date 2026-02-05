from robot import *
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "Genetic_algo"
    robot_id = -1

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=500, it_per_evaluation=400, replay_iterations=1000):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

        #params
        self.max_evals = evaluations
        self.it_per_evaluation = it_per_evaluation
        self.replay_iterations = replay_iterations

        #etat
        self.replay_mode = False
        self.eval_id = 0
        self.iter_in_eval = 0
        self.iter_in_replay = 0

        # =score effectif pour l individu qu on est entrain de tester
        self.score_eval = 0.0
        self.prev_trans = 0.0
        self.prev_rot = 0.0

        #algo genetique mu=1 + lambda=1 
        #parent
        self.parentParam = self.random_param()
        self.parentScore = float("-inf")   # inconnu tant qu'on n'a pas évalué un enfant

        #enfant donc individu teste mnt
        self.param = self.mutate_one(self.parentParam)  #on teste un enfant au depart

        #meilleur global pour info et replay
        self.bestScore = float("-inf")
        self.bestParam = self.param[:]
        self.bestEval = -1
        print("# eval_id, score_parent, best_so_far")

    def reset(self):
        super().reset()
        self.prev_trans = 0.0
        self.prev_rot = 0.0

    def random_param(self):
        return [random.randint(-1, 1) for _ in range(8)]

    def mutate_one(self, p):
        """Mutation: choisir 1 paramètre au hasard et changer sa valeur sans retirage."""
        q = p[:] #copie
        idx = random.randrange(len(q))
        old = q[idx]
        choices = [-1, 0, 1]
        choices.remove(old) #sans retirage, il sera forcement different
        q[idx] = random.choice(choices)
        return q

    def control(self, sensors):
        translation = math.tanh(self.param[0]+ self.param[1] * sensors[sensor_front_left]+ self.param[2] * sensors[sensor_front]+ self.param[3] * sensors[sensor_front_right])
        rotation = math.tanh(self.param[4]+ self.param[5] * sensors[sensor_front_left]+ self.param[6] * sensors[sensor_front]+ self.param[7] * sensors[sensor_front_right])
        return translation, rotation

    def update_score_effective(self):
        dtrans = self.log_sum_of_translation - self.prev_trans
        drot = self.log_sum_of_rotation - self.prev_rot
        self.prev_trans = self.log_sum_of_translation
        self.prev_rot = self.log_sum_of_rotation
        self.score_eval += dtrans * (1.0 - abs(drot))


    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        #replay
        if self.replay_mode:
            translation, rotation = self.control(sensors)
            self.iter_in_replay += 1
            if self.iter_in_replay >= self.replay_iterations:
                self.iter_in_replay = 0
                return 0, 0, True
            return translation, rotation, False

        #algo genetique, on evalue l enfant
        if self.iter_in_eval > 0:
            self.update_score_effective()

        #fin de l evaluation, l enfant a ete evalue sur 400 iterations
        if self.iter_in_eval >= self.it_per_evaluation:

            childScore = self.score_eval
            #selection mu=1 + lambda=1
            #si enfant meilleur, il devient le parent
            if self.parentScore == float("-inf") or childScore > self.parentScore:
                self.parentParam = self.param[:]
                self.parentScore = childScore
            #best global utile pour replay
            if self.parentScore > self.bestScore:
                self.bestScore = self.parentScore
                self.bestParam = self.parentParam[:]
                self.bestEval = self.eval_id
                print("[NEW BEST] eval =", self.bestEval, "score =", self.bestScore, "params =", self.bestParam)

            # affichage score du parent et best so far
            if self.bestScore == float("-inf"):
                print(self.eval_id, ",", self.parentScore, ",", self.parentScore)
            else:
                print(self.eval_id, ",", self.parentScore, ",", self.bestScore)

            # gégeneration suiv
            self.eval_id += 1

            #fin du budget, replay best
            if self.eval_id >= self.max_evals:
                self.replay_mode = True
                self.param = self.bestParam[:] #on rejoue le meilleur
                self.iter_in_replay = 0

                print("\n=== GENETIC (1+1) FINISHED ===")
                print("Best found at eval:", self.bestEval)
                print("Best score:", self.bestScore)
                print("Best params:", self.bestParam)
                print("=== REPLAY BEST FOREVER (chunks of 1000 iters) ===\n")

                #reset
                self.iter_in_eval = 0
                self.score_eval = 0.0
                return 0, 0, True

            #nouvel enfant:mutation du parent courant
            self.param = self.mutate_one(self.parentParam)

            #reset compteurs d evaluation
            self.iter_in_eval = 0
            self.score_eval = 0.0
            return 0, 0, True

        #commande pour evaluer l enfant
        translation, rotation = self.control(sensors)
        self.iter_in_eval += 1
        return translation, rotation, False
