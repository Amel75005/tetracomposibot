from robot import *
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "RandomSearch2"
    robot_id = -1

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",
                 evaluations=166, it_per_evaluation=400, replay_iterations=1000):

        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0

        #params perceptron
        self.param = self.random_param()

        #params
        self.max_evals = evaluations
        self.it_per_evaluation = it_per_evaluation
        self.replay_iterations = replay_iterations

        #mode recherche/replay
        self.replay_mode = False
        self.eval_id = 0
        self.iter_in_eval = 0
        self.iter_in_replay = 0

        #score effectid d une repetition
        self.score_eval = 0.0
        self.prev_trans = 0.0
        self.prev_rot = 0.0

        #on fait3 evals par stratefie
        self.rep = 0 #0 puis 1 puis 2
        self.score_strategy = 0.0 #simme des trois scores

        #meilleur individu
        self.bestScore = float("-inf")
        self.bestParam = self.param[:]
        self.bestEval = -1
        print("# eval_id, score_strategy(3 reps), best_so_far")

        #pour ecirire dnas un CSV
        self.run_id = random.randint(0, 10**9)
        self.csv_name = f"results_randomsearch2_{self.run_id}.csv"
        self.csv = open(self.csv_name, "w", encoding="utf-8")
        self.csv.write("eval,score,best,p0,p1,p2,p3,p4,p5,p6,p7\n")
        self.csv.flush()

    def reset(self):
        #orientation aleatoire a chaque reset pendant la recherche
        if not self.replay_mode:
            self.theta0 = random.uniform(0.0, 360.0)

        super().reset()
        #on remet nos refs a 0
        self.prev_trans = 0.0
        self.prev_rot = 0.0

    def random_param(self):
        return [random.randint(-1, 1) for _ in range(8)]

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

        #recherhce
        # maj score effectif
        if self.iter_in_eval > 0:
            self.update_score_effective()

        # fin d une repetition 400 iterations
        if self.iter_in_eval >= self.it_per_evaluation:
            #on ajoute le score de cette repetition au score de strategie
            self.score_strategy += self.score_eval
            self.rep += 1
            #reset des compteurs pour la prochaine repetotion
            self.iter_in_eval = 0
            self.score_eval = 0.0
            #si on a pas encore fait 3 repetitions on relance reset dans unennouvelle orientation
            if self.rep < 3:
                return 0, 0, True
            #sinon on a fini les 3 evals de la strategie
            score_total = self.score_strategy
            #on affiche le best
            if self.bestScore == float("-inf"):
                print(self.eval_id, ",", score_total, ",", score_total)
            else:
                print(self.eval_id, ",", score_total, ",", self.bestScore)

            if score_total > self.bestScore:
                self.bestScore = score_total
                self.bestParam = self.param[:]
                self.bestEval = self.eval_id
                print("[NEW BEST] eval =", self.bestEval, "score =", self.bestScore, "params =", self.bestParam)
            
            #pour ecorie dans le CSV 
            p = self.bestParam
            self.csv.write(f"{self.eval_id},{score_total},{self.bestScore},"
    f"{p[0]},{p[1]},{p[2]},{p[3]},{p[4]},{p[5]},{p[6]},{p[7]}\n")
            self.csv.flush()
            #prochaine strat
            self.eval_id += 1

            

            #si budget fini replay
            if self.eval_id >= self.max_evals:
                #on ferme le fichiers CSV
                self.csv.close()
                self.replay_mode = True
                self.param = self.bestParam[:]
                self.iter_in_replay = 0

                print("\n=== RANDOMSEARCH2 FINISHED ===")
                print("Best found at eval:", self.bestEval)
                print("Best score:", self.bestScore)
                print("Best params:", self.bestParam)
                print("=== REPLAY BEST FOREVER (chunks of 1000 iters) ===\n")
                #reset
                self.rep = 0
                self.score_strategy = 0.0
                return 0, 0, True

            #nouvelle strategie + reset des variables
            self.param = self.random_param()
            self.rep = 0
            self.score_strategy = 0.0
            return 0, 0, True

        # commande pendant une repetition
        translation, rotation = self.control(sensors)
        self.iter_in_eval += 1
        return translation, rotation, False
