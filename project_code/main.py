import math
import random

import evaluation
import initialization
import mutation
import numpy
import parent_selection
import recombination
import survivor_selection
import traffic_network


def main():
   
    # building our graph
    toronto_graph = traffic_network.graph()
    toronto_graph.build()

    # radomly picking a start and end node to run on
    start_node, end_node = random.sample(list(toronto_graph.get_nodes()), 2)
    
    # hyperparameters
    popsize              = 5
    routes_per_member    = 3
    xover_rate           = "unknown"
    xover_strategy       = recombination.exhaustive_crossover
    mut_rate             = "unknown"
    gen_limit            = 300

    # initialize population - works
    population = []
    for _ in range(popsize):
        individual = [toronto_graph.dijkstra(start_node, end_node) for _ in range(routes_per_member)]
        population.append(individual)
    #print(population)
        
    # calculate fitnesses of original population - works
    route_fitnesses      = [[evaluation.fitness(toronto_graph, route) for route in individual] for individual in population]
    individual_fitnesses = [round(sum(individual_routes), 2) for individual_routes in route_fitnesses]
    #print(route_fitnesses)
    #print(individual_fitnesses)

    # initialize the generation counter
    gen = 0
    # evolution begins
    while gen < gen_limit:
        # perform crossovers
        crossover_offspring = []
        for _ in range(round(math.sqrt(popsize**2 - popsize/2))):
            selected_parents = random.sample(population, 2)
            # once we code xovers this should work
            single_crossover_offspring = xover_strategy(selected_parents)
            crossover_offspring.append(single_crossover_offspring)
        # print(f'{crossover_offspring}, num pairs = {len(crossover_offspring)}')
    
        # reproduction
        
        # generate offspring
        
        # recombination
            
        # mutation

        # organize the population of next generation
        
        gen = gen + 1  # update the generation counter
        
    # evolution ends
    
    # print solutions


# end of main

if __name__ == "__main__":
    main()
