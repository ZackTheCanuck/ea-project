from operator import itemgetter


def select_survivors(pop, mut_pop, xover_pop, num_survivors):
    population_fitnesses          = [(i.get_overall_fitness(), i) for i in pop]
    mutated_population_fitnesses  = [(i.get_overall_fitness(), i) for i in mut_pop]
    crossover_offspring_fitnesses = [(i.get_overall_fitness(), i) for i in xover_pop]

    # our fitness is trying to be minimized so we use min here
    if min(population_fitnesses, key=itemgetter(0))[0] < min(crossover_offspring_fitnesses, key=itemgetter(0))[0]:
        crossover_offspring_fitnesses = []

    total_population = population_fitnesses + mutated_population_fitnesses + crossover_offspring_fitnesses

    sorted_total_population = sorted(total_population, key=itemgetter(0))
    return [ind[1] for ind in sorted_total_population][:num_survivors]