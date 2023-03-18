import random

#initialize population with random routes
def initialize_population(graph, start, end, population_size, n_routes):
    population = []
    for i in range(population_size):
        individual = []
        for x in range(n_routes):
            route = random_route(graph, start, end)
            individual.append(route)
        population.append(individual)
    return population

#Generate random routes between start and end nodes in the graph
def random_route(graph, start, end):
    route = [start]
    current_node = start
    while current_node != end:
        neighbors = list(graph.neighbors(current_node))
        next_node = random.choice(neighbors)
        route.append(next_node)
        current_node = next_node
    return route

