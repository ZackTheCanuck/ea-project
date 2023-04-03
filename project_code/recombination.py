import numpy as np
import itertools
import population_individual
from diversity import *

def exhaustive_crossover(parents):
    parent1 = parents[0]
    parent2 = parents[1]
    parent1_routes = parent1.get_routes()
    parent2_routes = parent2.get_routes()
    n = parent1.get_num_routes()

    combined_routes = parent1_routes + parent2_routes
    all_combinations = list(itertools.combinations(combined_routes, n))

    max_diversity = -1
    best_combination = None

    for combination in all_combinations:
        # Calculate diversity score for this combination
        diversity_score = diversity_func(combination)
        
        # If the current combination has a higher diversity score than the previous maximum,
        # update the maximum diversity score and store the current combination.
        if diversity_score > max_diversity:
            max_diversity = diversity_score
            best_combination = combination

    for index, route in enumerate(best_combination):
        parent1.update_route_at_index(index, route)

    return parent1


def greedy_crossover(parents):                                          
    """Constructs one new route set following the specified greedy crossover algo"""
    # Randomly select one route
    comb_routes = parents[0].get_routes() + parents[1].get_routes()
    rand_idx = np.random.randint(0, len(comb_routes))                                   # combine routes into one array
    r = comb_routes[rand_idx]                                                           # simplest init is to fill arr with the random val
    comb_routes.pop(rand_idx)                                                           # delete that val from the vals to be selected
    
    # Choose subset of n-1 routes which maximizes diversity_func()
    n = parents[0].get_num_routes()
    subsets = [route_set for route_set in itertools.combinations_with_replacement(comb_routes, n-1)]    

    ordered_idx = np.argsort([diversity_func(route_set) for route_set in subsets])      # sort the genes according to diversity function   
    new_routes = list(subsets[ordered_idx[0]])                                          # get routes which max diversity
    new_routes = [r] + new_routes                                                       # insert random route into position 0

    child = population_individual.individual(parents[0].get_graph(), routes=new_routes) # initialize child
    return child
                                                                                    
    
def randomized_greedy_crossover(parents):
    """Constructs one new route set following the specified randomized greedy crossover algo"""
    # Randomly select one route
    comb_routes = parents[0].get_routes() + parents[1].get_routes()
    rand_idx = np.random.randint(0, len(comb_routes))                                   # combine routes into one array
    r = comb_routes[rand_idx]                                                           # simplest init is to fill arr with the random val
    comb_routes.pop(rand_idx)                                                           # delete that val from the vals to be selected
    n = parents[0].get_num_routes()
    divs = np.array([diversity_func(route) for route in comb_routes])                   # get diversities
    rte_idx = np.random.choice(2*n-1, n-1, p=divs/np.sum(divs))                         # randomly sample route indices using diversity as prob
    new_routes = [comb_routes[i] for i in rte_idx]                                      # get corresponding routes
    new_routes = [r] + new_routes                                                       # insert random route into position 0
    child = population_individual.individual(parents[0].get_graph(), routes=new_routes) # initialize child
    return child