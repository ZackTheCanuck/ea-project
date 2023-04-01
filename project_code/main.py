import copy
import math
import os
import random
import time

import graph_helpers
import hyperparameters
import metrics
import mutation
import numpy
import population_individual
import recombination
import survivor_selection
from initialization import initialize_populations, migrate


def main():

    # building our graph
    toronto_graph, geodata = graph_helpers.build_graph()
    
    runs_generational_average_fitness = []

    runs_best_result        = []
    runs_average_result     = []

    execution_times         = []
    average_execution_time  = []

    # mutation parameters
    mut_ops             = (mutation.new_route, mutation.random_p, mutation.link_wp, mutation.ex_segment)
    mut_ops_weights     = [30, 60, 30, 15]
    ex_segment_counter  = 6  # count how many generations since last using ex_segment - starting this at 6 lets us increase its weight in the first 6 generations properly

    # hyperparameters
    START_NODE, END_NODE = random.sample(list(toronto_graph.nodes), 2)
    RUNS_PER_ROUTE       = hyperparameters.num_runs
    POPSIZE              = hyperparameters.population_size
    XOVER                = hyperparameters.crossover_strategy
    GEN_LIMIT            = hyperparameters.max_generations
    NUM_ISLANDS          = hyperparameters.num_islands
    MIGRATION_INTERVAL   = hyperparameters.migration_interval
    NUM_MIGRANTS         = hyperparameters.num_migrants

    run_metrics = metrics.run_metrics(START_NODE, END_NODE)
    run_metrics.save_hyperparameters()
    
    for run in range(RUNS_PER_ROUTE):
        print(f'Starting run {run+1} of {RUNS_PER_ROUTE} from {START_NODE} -> {END_NODE}')
        # start timer
        start_time = time.perf_counter()
        # initialize multiple populations
        populations, all_unique_routes = initialize_populations(toronto_graph, START_NODE, END_NODE, POPSIZE, NUM_ISLANDS)
        
        generation_average_fitness = []
        total_fitness  = 0
        total_pop_size = 0
        for pop in populations:
            for ind in pop:
                total_fitness  += ind.get_overall_fitness()
                total_pop_size += 1
        generation_average_fitness.append(total_fitness/total_pop_size)
        # initialize the generation counter
        for gen in range(GEN_LIMIT):
            new_populations = []
            ex_segment_used = False
            for population in populations:
            # perform crossovers
                crossover_offspring = []
                # parent selection done with random sampling
                for _ in range(round(math.sqrt(POPSIZE**2 - POPSIZE/2))):
                    selected_parents = copy.deepcopy(random.sample(population, 2))
                    single_crossover_offspring = XOVER(selected_parents)
                    crossover_offspring.append(single_crossover_offspring)
                # print(f'{crossover_offspring}, num pairs = {len(crossover_offspring)}')
            
                mutated_population = copy.deepcopy(population)

                for individual in mutated_population:
                    num_mutations = max(1, numpy.random.poisson(1.5))
                    mutations_to_perform = random.choices(mut_ops, weights=mut_ops_weights, k=num_mutations)
                    if mutation.ex_segment in mutations_to_perform:
                        mutations_to_perform = [mutation.ex_segment]
                        ex_segment_used = True
                    # apply mutations
                    for mutation_operator in mutations_to_perform:
                        individual = mutation_operator(individual, all_unique_routes, toronto_graph, START_NODE, END_NODE)
                    
                    # update all_unique_routes in the mutation process
                    for route in individual.get_routes():
                        if route not in all_unique_routes:
                            all_unique_routes.append(route)
                        
                population = survivor_selection.select_survivors(population, mutated_population, crossover_offspring, POPSIZE)
                new_populations.append(population)
                
            # migrate every migration_interval
            if gen % MIGRATION_INTERVAL == 0 and gen != 0:
                new_populations = migrate(new_populations, NUM_MIGRANTS)
            
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

            # get info from the populations for metrics
            total_fitness = 0
            total_pop_size = 0
            for pop in populations:
                for ind in pop:
                    total_fitness  += ind.get_overall_fitness()
                    total_pop_size += 1
            generation_average_fitness.append(total_fitness/total_pop_size)

            # break early if population fitness hasnt changed for 10 generations
            if len(generation_average_fitness) >= 10 and len(set(generation_average_fitness[-10:])) == 1:
                print(f'Ending early at generation {gen}')
                break

        runs_generational_average_fitness.append(generation_average_fitness)
        execution_time = time.perf_counter() - start_time
        execution_times.append(execution_time)
        average_execution_time.append(sum(execution_times)/len(execution_times))
        # evolution ends
        
        # print solutions
        best_run_solution_per_island = []
        for i, population in enumerate(populations):
            best_solution = min(population, key=lambda x: x.get_overall_fitness())
            best_solution_fitness = best_solution.get_overall_fitness()
            print(f"Best solution from population {i + 1}: {best_solution}, fitness = {best_solution_fitness}")
            best_run_solution_per_island.append(best_solution_fitness)
            #best_solution.display(geodata)
        runs_average_result.append(sum(best_run_solution_per_island)/len(best_run_solution_per_island))
        runs_best_result.append(min(best_run_solution_per_island))

    run_metrics.create_fitness_plot(runs_generational_average_fitness)
    run_metrics.create_execution_times_plot(execution_times, average_execution_time)
    run_metrics.create_results_plot(runs_best_result, runs_average_result)

# end of main

if __name__ == "__main__":
    main()
