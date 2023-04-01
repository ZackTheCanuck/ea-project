import os

import recombination
import shortest_path_algorithms

# population individual HPs
routes_per_individual = 3
shortest_path_algo    = shortest_path_algorithms.dijkstra

# main HPs
proj_root = os.path.dirname(os.path.dirname(__file__))
num_runs  = 10
population_size = 5
crossover_strategy = recombination.exhaustive_crossover
max_generations = 200
num_islands = 3
migration_interval = 10
num_migrants = 1