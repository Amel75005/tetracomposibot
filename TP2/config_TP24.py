import arenas
import genetic_algorithms

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
replay_iterations = 1000

max_iterations = evaluations * it_per_evaluation + 5000
#pour voir le replay

def initialize_robots(arena_size=-1, particle_box=-1):
    x_center = arena_size // 2 - particle_box / 2
    y_center = arena_size // 2 - particle_box / 2
    robots = []
    robots.append(genetic_algorithms.Robot_player(x_center, y_center, 0, name="Genetic_algo", team="A"))
    return robots
