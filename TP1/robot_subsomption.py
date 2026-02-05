
from robot import * 

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "Compote"
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
        
        #activation des murs : hatewall
        wall_front = 1.0 - sensor_to_wall[sensor_front]
        wall_front_left = 1.0 - sensor_to_wall[sensor_front_left]
        wall_front_right = 1.0 - sensor_to_wall[sensor_front_right]
        #activation des robots : lovebot
        bot_front = 1.0 - sensor_to_robot[sensor_front]
        bot_front_left = 1.0 - sensor_to_robot[sensor_front_left]
        bot_front_right = 1.0 - sensor_to_robot[sensor_front_right]
        #danger de mur 
        wall_danger = wall_front + wall_front_left + wall_front_right
        #pas de subsomption, oin evite les murs hatewall
        if self.robot_id != 0:
            left  = wall_front_left + 0.5*wall_front
            right = wall_front_right + 0.5*wall_front
            rotation = (right - left) * 1.2
            translation = 0.6 - 0.8*wall_danger
            translation = max(0.0, min(1.0, translation))
            rotation = max(-1.0, min(1.0, rotation))
            self.iteration += 1
            return translation, rotation, False
        #subsomption 
        #si un des trois n est pas nul donc on voit un robot
        see_robot = (bot_front + bot_front_left + bot_front_right) > 0.01
        #priorite 1 on evite les murs 
        #si un mur est proche devant 
        if wall_danger > 0.4:
            left  = wall_front_left + 0.5*wall_front
            right = wall_front_right + 0.5*wall_front
            rotation = (right - left) * 1.2
            translation = 0.6 - 0.8*(wall_front + wall_front_left + wall_front_right)
        #priorite 2 on va vers les robots
        elif see_robot:
            left  = bot_front_left
            right = bot_front_right
            rotation = (left - right) * 1.2
            translation = 0.2 + 0.7*(bot_front + bot_front_left + bot_front_right)
        #priorite 3 on avance tout droit
        else:
            rotation = 0.0
            translation = 0.5
        #on borne
        translation = max(0.0, min(1.0, translation))
        rotation = max(-1.0, min(1.0, rotation))
        self.iteration += 1
        return translation, rotation, False
    
        