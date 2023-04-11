import timeit
import shortest_path_algorithms

# timeit(number=1000000)
# Time number executions of the main statement. This executes the setup statement once, and then returns the time it takes to execute
# the main statement a number of times, measured in seconds as a float. The argument is the number of times through the loop, defaulting to one million.
# The main statement, the setup statement and the timer function to be used are passed to the constructor
NUM_EXECS = 100_000
def run_time_test(route):
    
    setup = f'''
import timeit

import graph_helpers
import hyperparameters
import population_individual
import shortest_path_algorithms

toronto_graph, geodata = graph_helpers.build_graph()
START_NODE, END_NODE = {route}
SPA, SPA_VAR         = (shortest_path_algorithms.bellman_ford, shortest_path_algorithms.bellman_ford_variance)

'''
    my_code = '''
ROUTES_PER_IND = hyperparameters.routes_per_individual
best_route = [SPA(toronto_graph, START_NODE, END_NODE)] * ROUTES_PER_IND
baseline_fitness_ind = population_individual.individual(toronto_graph, START_NODE, END_NODE, best_route)
baseline_fitness = baseline_fitness_ind.get_overall_fitness()
'''
    # timeit statement
    exec_time = timeit.timeit(setup=setup, stmt=my_code, number=NUM_EXECS)
    print(f'Average time to execute route {route} with BF = {exec_time / NUM_EXECS}')

def run_time_tests():
    TEST_ROUTES = [(13, 6), (116, 117), (85,15), (5, 139), (34, 21), (1, 11)]
    for route in TEST_ROUTES:
        run_time_test(route)

run_time_tests()