from population_individual import *
import numpy as np

def diversity_func(individual):
    """Returns the diversity score for an individual."""
    edge_arr = np.hstack(individual.get_routes())
    _, counts = np.unique(edge_arr, return_counts=True)                 # get unique edges and counts of each
    sum_of_sq = np.sum(np.square(counts))                               # take the sum of squares of the counts
    singles = len(np.where(counts == 1)[0])                             # get the number of edges with exactly 1 occurence
    denom = max(1,singles)

    return sum_of_sq/denom
