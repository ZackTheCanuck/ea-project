import copy
import math
import random

import evaluation
import graph_helpers
import initialization
import mutation
import numpy
import parent_selection
import population_individual
import recombination
import survivor_selection


def main():
   
    # building our graph
    toronto_graph = graph_helpers.build_graph()

    # radomly picking a start and end node to run on
    start_node, end_node = random.sample(list(toronto_graph.nodes), 2)
    
    # hyperparameters
    popsize              = 5
    xover_strategy       = recombination.exhaustive_crossover
    mut_ops              = (mutation.new_route, mutation.random_p, mutation.link_wp, mutation.ex_segment)
    mut_ops_weights      = [30, 60, 30, 15]
    gen_limit            = 1

    # initialize population and fitnesses - works
    population   = []
    for _ in range(popsize):
        population.append(population_individual.individual(toronto_graph, start_node, end_node))
        
    # fitnesses of individuals calculated on the fly - works

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
            crossover_offspring.extend(single_crossover_offspring)
        # print(f'{crossover_offspring}, num pairs = {len(crossover_offspring)}')
    
        mutated_population = copy.deepcopy(population)

        for individual in mutated_population:
            num_mutations = max(1, numpy.random.poisson(1.5))
            mutations_to_perform = random.choices(mut_ops, weights=mut_ops_weights, k=num_mutations)
            # TODO: update mut_ops_weights over generations according to the paper
            if mutation.ex_segment in mutations_to_perform:
                mutations_to_perform = [mutation.ex_segment]
            # apply mutations
            for mutation_operator in mutations_to_perform:
                individual = mutation_operator(individual)
                
        population_dict          = {i:i.get_overall_fitness() for i in population}
        mutated_population_dict  = {i:i.get_overall_fitness() for i in mutated_population}
        crossover_offspring_dict = {i:i.get_overall_fitness() for i in crossover_offspring}

        #print(len(population_dict), len(mutated_population_dict), len(crossover_offspring_dict))
        
        # our fitness is trying to be minimized so we use min here
        if min(population_dict.values()) < min(crossover_offspring_dict.values()):
            print('Dropping all xovers')
            crossover_offspring = []

        #print(len(population_dict), len(mutated_population_dict), len(crossover_offspring_dict))
        total_population_dict = dict(population_dict)
        total_population_dict.update(mutated_population_dict)
        total_population_dict.update(crossover_offspring_dict)
        #print(len(total_population_dict))

        sorted_total_population = sorted(total_population_dict.items(), key=lambda item:item[1])
        population = [list(ind)[0] for ind in sorted_total_population][:popsize]
        #print(len(population))
        
        gen = gen + 1  # update the generation counter
        
    # evolution ends
    
    # print solutions
    print(population[0])


# end of main

if __name__ == "__main__":
    main()
