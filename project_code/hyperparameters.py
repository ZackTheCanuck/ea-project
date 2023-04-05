import os

import shortest_path_algorithms

# population individual HPs
routes_per_individual = 3
#! make sure SPA is correct for your test runs
shortest_path_algo = (shortest_path_algorithms.a_star, shortest_path_algorithms.a_star_variance)

# main HPs
proj_root = os.path.dirname(os.path.dirname(__file__))
num_runs  = 75
population_size = 5
max_generations = 200
num_islands = 3
migration_interval = 10
num_migrants = 1