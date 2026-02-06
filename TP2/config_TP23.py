import arenas
import robot_randomsearch2

display_mode = 1
arena = 1
position = False 

display_welcome_message = False
verbose_minimal_progress = False
display_robot_stats = False
display_team_stats = False
display_tournament_results = False
display_time_stats = True

evaluations = 500
it_per_evaluation = 400
repetitons = 3
max_iterations = evaluations * repetitons * it_per_evaluation + 5000
#pour voir le replay

def initialize_robots(arena_size=-1, particle_box=-1):
    x_center = arena_size // 2 - particle_box / 2
    y_center = arena_size // 2 - particle_box / 2
    robots = []
    robots.append(robot_randomsearch2.Robot_player(x_center, y_center, 0, name="RandomSearch2", team="A"))
    return robots
