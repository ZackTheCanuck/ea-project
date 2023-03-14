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
    mut_rate             = "unknown"
    gen_limit            = 300

    # initialize population - works
    population = []
    for _ in range(popsize):
        individual = [toronto_graph.dijkstra(start_node, end_node) for _ in range(routes_per_member)]
        population.append(individual)
    print(population)
        
    # calculate fitnesses of original population - works
    route_fitnesses      = [[evaluation.fitness(toronto_graph, route) for route in individual] for individual in population]
    individual_fitnesses = [round(sum(individual_routes), 2) for individual_routes in route_fitnesses]
    print(route_fitnesses)
    print(individual_fitnesses)

    # initialize the generation counter
    gen = 0
    # evolution begins
    while gen < gen_limit:
        
        # pick parents: repeat √︁(𝜇^2 − 𝜇/2) times
        # select two individuals uniformly at random
    
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
