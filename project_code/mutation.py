# mutation methods
import ea_helpers
import numpy as np
import shortest_path_algorithms


# select a route to mutate inversely proportional to how often the route appears in the individual
# this makes sense because it assumes there is some reason we have evolved to generate a route multiple times,
# therefore it is more likely beneficial that we keep it
def new_route(individual, all_routes, graph, start, end):
    probabilities    = ea_helpers.get_inverse_traffic_flow_probabilities(individual, all_routes)
    all_routes_index = np.random.choice(range(len(all_routes)), p=probabilities)
    route_to_replace = all_routes[all_routes_index]
    
    route_index = individual.routes.index(route_to_replace)
    
    new_route = shortest_path_algorithms.dijkstra(graph, start, end)
    individual.routes[route_index] = new_route
    if new_route not in all_routes:
        all_routes.append(new_route)
    
    return individual

def random_p(individual, all_routes, graph, start, end):
    return individual

def link_wp(individual, all_routes, graph, start, end):
    return individual

def ex_segment(individual, all_routes, graph, start, end):
    return individual