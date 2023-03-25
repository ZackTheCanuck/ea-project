import random
from population_individual import individual

#Create multiple populations, store unique_routes for each population
def initialize_populations(graph, start_node, end_node, popsize, num_populations):
    populations = []
    all_unique_routes = []

    for i in range(num_populations):
        population = []
        for j in range(popsize):
            ind = individual(graph, start_node, end_node)
            population.append(ind)
            for route in ind.routes:
                if route not in all_unique_routes:
                    all_unique_routes.append(route)
        populations.append(population)

    return populations, all_unique_routes

def migrate(populations, num_migrants):
    num_populations = len(populations)
    # Loop through each population to perform migration
    for i in range(num_populations):
        migrants = random.sample(populations[i], num_migrants)  # Randomly select migrants from the current population
        
        # Remove the selected migrants from the source population
        for migrant in migrants:
            populations[i].remove(migrant)

        target_island = (i + 1) % num_populations  # Determine the target island for migration
        # Add migrants to the target island population
        populations[target_island].extend(migrants)
    return populations
