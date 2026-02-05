# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Amel BEN CHABANE 21304456
#  Prénom Nom No_étudiant/e : Tassadit AKSAS 21302943
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 
import random
nb_robots = 0

class Robot_player(Robot):

    team_name = "Tasmel"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        #on s est inspire du tp1, comportement hateWall
        sensor_to_wall = []
        #on separe murs 1 et robots 2 et vides autres valeurs
        for i in range(8):
            if sensor_view[i] == 1: #la c est un mur
                sensor_to_wall.append(sensors[i])
            else: #robot ou vide on ignore
                sensor_to_wall.append(1.0)
        
        #on active les murs : 1-dist
        wall_front = 1.0 - sensor_to_wall[sensor_front]
        wall_front_left = 1.0 - sensor_to_wall[sensor_front_left]
        wall_front_right = 1.0 - sensor_to_wall[sensor_front_right]
        #si mur a gauche on active a gauche, si a droite on active a droite
        #si il est devant, il n est ni a gauche ni a droite mais danger pour les deux
        left  = wall_front_left + 0.5 * wall_front
        right = wall_front_right + 0.5 * wall_front
        #on fuit le mur
        rotation = (right - left) * 1.2
        #on ralentit quand on est proche du mur
        translation = 0.6 - 0.8 * (wall_front + wall_front_left + wall_front_right)
        #on borne
        translation = max(0.0, min(1.0, translation))
        rotation = max(-1.0, min(1.0, rotation))
        return translation, rotation, False

