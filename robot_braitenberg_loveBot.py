
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
        #activation des robots uniquement car les murs sont ignores
        active_front = 1.0 - sensor_to_robot[sensor_front]
        active_front_left = 1.0 - sensor_to_robot[sensor_front_left]
        active_front_right = 1.0 - sensor_to_robot[sensor_front_right]
        active_left = 1.0 - sensor_to_robot[sensor_left]
        active_right = 1.0 - sensor_to_robot[sensor_right]
        active_rear_left = 1.0 - sensor_to_robot[sensor_rear_left]
        active_rear_right = 1.0 - sensor_to_robot[sensor_rear_right]
        #gauche droite et devant pour les robots seulement
        left = active_front_left + active_left + active_rear_left 
        right = active_front_right + active_right + active_rear_right
        front = active_front
        #rotation love on tourne vers le robot
        rotation = (left - right)*1.0
        #translation pour avancer et accelerer quand on voit un robot 
        translation = 0.2 + 0.6 *(front+active_front_left+active_front_right)
        #on borne
        translation = max(0.0, min(1.0, translation))
        rotation = max(-1.0, min(1.0, rotation))
        self.iteration = self.iteration + 1        
        return translation, rotation, False
