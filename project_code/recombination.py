import numpy as np
import itertools
import diversity

def exhaustive_crossover(parents):
    parent1_routes = parents[0].routes
    parent2_routes = parents[1].routes
    n = len(parent1_routes)

    combined_routes = parent1_routes + parent2_routes
    all_combinations = list(itertools.combinations(combined_routes, n))

    max_diversity = -1
    best_combination = None

    for combination in all_combinations:
        # Calculate diversity score for this combination
        diversity_score = diversity.diversity_func(combination)
        
        # If the current combination has a higher diversity score than the previous maximum,
        # update the maximum diversity score and store the current combination.
        if diversity_score > max_diversity:
            max_diversity = diversity_score
            best_combination = combination

    return list(best_combination)


def greedy_crossover(parents, diversity_func):                                  # diversity_func is placeholder to be implemented and imported
    """Constructs one new route set following the specified greedy crossover algo"""
    # Randomly select one route
    comb_chroms = np.concatenate((parents[0], parents[1]))                      # combine chromosomes into one array
    random_index = np.random.randint(0, len(comb_chroms))       
    r = comb_chroms[random_index]                                               # simplest init is to fill arr with the random val
    np.delete(comb_chroms, random_index)                                        # delete that val from the vals to be selected
    
    # Select n-1 routes greedily
    n = len(parents[0])
    sorted_genes = np.sort([diversity_func(allele) for allele in comb_chroms])  # sort the genes according to diversity function    
    child = sorted_genes[:n-1]                                                  # greedily select the n-1 most diverse routes
    child.insert(r,0)                                                           # insert random route into position 0 (optional?)

    return child

def randomized_greedy_crossover(parents, diversity_func):
    """Constructs one new route set following the specified randomized greedy crossover algo"""
    # Randomly select one route
    comb_chroms = np.concatenate((parents[0], parents[1]))  # combine chromosomes into one array
    random_index = np.random.randint(0, len(comb_chroms))
    r = comb_chroms[random_index]  # simplest init is to fill arr with the random val
    np.delete(comb_chroms, random_index)  # delete that val from the vals to be selected

    # Select n-1 routes greedily
    n = len(parents[0])
    diversities = [diversity_func(allele) for allele in comb_chroms]  # Get diversities
    child = []
    for i in range(n-1):
        child.append(np.random.choice(comb_chroms, p=diversities))  # Sample from routes using the diversity as the probability
    child.insert(r, 0)  # insert random route into position 0 (optional?)

    return child