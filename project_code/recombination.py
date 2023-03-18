import numpy as np

def exhaustive_crossover(parents):
    return parents

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

def randomized_greedy_crossover():
    return