# mutation methods
import random

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


def random_p(individual, all_unique_routes, graph, start_node, end_node):

    # Choose a random subset of routes proportional to their inverse traffic flow
    probabilities = ea_helpers.get_inverse_traffic_flow_probabilities(individual, all_unique_routes)
    # Select a random subset of route indices from all_unique_routes based on probabilities
    selected_routes_indices = np.random.choice(len(all_unique_routes), size=len(individual.routes) // 2, replace=False, p=probabilities)
    # Get the routes corresponding to the selected indices
    selected_routes = []
    for i in selected_routes_indices:
        selected_routes.append(all_unique_routes[i])
    for route in selected_routes:
        # Choose a start node and destination node
        route_length = len(route)
        start_index = random.randint(0, route_length - 2)
        max_subroute_length = route_length - start_index
        subroute_length = max(min(abs(int(np.random.normal(0.25 * route_length, 0.5 * route_length))), max_subroute_length), 2)
        end_index = start_index + subroute_length - 1
        # Replace subsegment with a new random route
        new_subroute = shortest_path_algorithms.dijkstra(graph, route[start_index], route[end_index])
        new_route = route[:start_index] + new_subroute[:-1] + route[end_index:]
        new_route = ea_helpers.remove_cycles(new_route)
        individual.routes[individual.routes.index(route)] = new_route

    # Update all_unique_routes with new routes
    for route in individual.routes:
        if route not in all_unique_routes:
            all_unique_routes.append(route)

    return individual

def link_wp(individual, all_routes, graph, start, end):

    return individual

def ex_segment(individual, all_routes, graph, start, end):
    return individual