
from robot import * 

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "Dumb"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\t\tsensors to wall  =",sensor_to_wall)
                print ("\t\tsensors to robot =",sensor_to_robot)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)
        #activation des murs uniquement car les robots sont ignores
        active_wall  = [1.0 - d for d in sensor_to_wall]
        #gauche droite et devant pour les murs seulement
        left = active_wall[sensor_front_left]
        right = active_wall[sensor_front_right]
        front = active_wall[sensor_front]
        #rotation love on tourne vers le mur au lieu de l eviter
        rotation = (left - right)*1.0
        #translation pour avancer un peu et accelerer quand on voit un mur
        translation = 0.3 + 0.4 *(front+left+right)
        #on borne
        translation = max(0.0, min(1.0, translation))
        rotation = max(-1.0, min(1.0, rotation))
        self.iteration = self.iteration + 1        
        return translation, rotation, False
