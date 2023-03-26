import copy
import math
import random
from operator import itemgetter

import evaluation
import graph_helpers
import initialization
import mutation
import numpy
import parent_selection
import population_individual
import recombination
import survivor_selection
from initialization import initialize_populations, migrate


def main():
   
    # building our graph
    toronto_graph, geodata = graph_helpers.build_graph()

    # randomly picking a start and end node to run on
    start_node, end_node = random.sample(list(toronto_graph.nodes), 2)
    print(f'Starting run from {start_node} -> {end_node}')
    
    # hyperparameters
    popsize              = 5
    xover_strategy       = recombination.exhaustive_crossover
    mut_ops              = (mutation.new_route, mutation.random_p, mutation.link_wp, mutation.ex_segment)
    mut_ops_weights      = [30, 60, 30, 15]
    gen_limit            = 200
    num_populations      = 3  # Add the number of populations you want to create here
    migration_interval   = 10
    num_migrants         = 1
    ex_segment_counter   = 6  # count how many generations since last using ex_segment - starting this at 6 lets us increase its weight in the first 6 generations properly

    # initialize multiple populations
    populations, all_unique_routes = initialize_populations(toronto_graph, start_node, end_node, popsize, num_populations)
     
    # fitnesses of individuals calculated on the fly - works

    # initialize the generation counter
    for gen in range(gen_limit):
        new_populations = []
        for population in populations:
        # perform crossovers
            crossover_offspring = []
            for _ in range(round(math.sqrt(popsize**2 - popsize/2))):
                selected_parents = copy.deepcopy(random.sample(population, 2))
                # once we code xovers this should work
                single_crossover_offspring = xover_strategy(selected_parents)
                crossover_offspring.extend(single_crossover_offspring)
            # print(f'{crossover_offspring}, num pairs = {len(crossover_offspring)}')
        
            mutated_population = copy.deepcopy(population)
            ex_segment_used = False

            for individual in mutated_population:
                num_mutations = max(1, numpy.random.poisson(1.5))
                mutations_to_perform = random.choices(mut_ops, weights=mut_ops_weights, k=num_mutations)
                if mutation.ex_segment in mutations_to_perform:
                    mutations_to_perform = [mutation.ex_segment]
                    ex_segment_used = True
                # apply mutations
                for mutation_operator in mutations_to_perform:
                    individual = mutation_operator(individual, all_unique_routes, toronto_graph, start_node, end_node)
                
                # update all_unique_routes in the mutation process
                for route in individual.routes:
                    if route not in all_unique_routes:
                        all_unique_routes.append(route)
                    
            population_fitnesses          = [(i.get_overall_fitness(), i) for i in population]
            mutated_population_fitnesses  = [(i.get_overall_fitness(), i) for i in mutated_population]
            crossover_offspring_fitnesses = [(i.get_overall_fitness(), i) for i in crossover_offspring]

            # our fitness is trying to be minimized so we use min here
            if min(population_fitnesses, key=itemgetter(0))[0] < min(crossover_offspring_fitnesses, key=itemgetter(0))[0]:
                crossover_offspring_fitnesses = []

            total_population = population_fitnesses + mutated_population_fitnesses + crossover_offspring_fitnesses

            sorted_total_population = sorted(total_population, key=itemgetter(0))
            population = [ind[1] for ind in sorted_total_population][:popsize]
            
            new_populations.append(population)
            
        #migrate every migration_interval
        if gen % migration_interval == 0 and gen != 0:
            new_populations = migrate(new_populations, num_migrants)
        
        populations = new_populations

        # update mutation operators frequency
        # new_route updated so that  it is 30 for the first 10 iterations, and then lowered linearly such that it reaches 1 at iteration 200
        if gen >= 10:
            current_new_route_weight = mut_ops_weights[0]
            mut_ops_weights[0] = max(current_new_route_weight - 29/190, 1)
        # ex_segment updated so that if it was used within the last 6 iterations its weight is 0
        # otherwise, it starts at 15 and is increased linearly to 30, depending on the iterations without improvement
        if ex_segment_used:
            mut_ops_weights[3] = 0
            ex_segment_counter = 0
        else:
            ex_segment_counter += 1
            if ex_segment_counter > 6:
                mut_ops_weights[3] = min(15 + (0.5 * (ex_segment_counter - 6)), 30)
        
    # evolution ends
    
    # print solutions
    for i, population in enumerate(populations):
        best_solution = min(population, key=lambda x: x.get_overall_fitness())
        print(f"Best solution from population {i + 1}: {best_solution}, fitness = {best_solution.get_overall_fitness()}")
        #best_solution.display(geodata)


# end of main

if __name__ == "__main__":
    main()
