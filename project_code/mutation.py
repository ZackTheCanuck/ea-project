# mutation methods
import ea_helpers
import numpy as np
import shortest_path_algorithms
import random


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
    temp_ind = individual
    try:
        # Choose a random subset of routes proportional to their inverse traffic flow
        probabilities = ea_helpers.get_inverse_traffic_flow_probabilities(individual, all_unique_routes)
        selected_routes = np.random.choice(individual.routes, size=len(individual.routes) // 2, replace=False, p=probabilities)

        # Replace subsegments of each selected route
        for route in selected_routes:
            # Choose a start node and destination node
            start_index = random.randint(0, len(route) - 1)
            route_length = len(route)
            end_index = start_index + round(np.random.normal(0.25 * route_length, 0.5 * route_length))
            end_index = min(max(end_index, 0), route_length - 1)  # Ensure destination index is within valid range

            # Replace subsegment with a new random route
            new_route = shortest_path_algorithms.dijkstra(graph, route[start_index], route[end_index])
            individual.routes[individual.routes.index(route)] = new_route

        # Update all_unique_routes with new routes
        for route in individual.routes:
            if route not in all_unique_routes:
                all_unique_routes.append(route)
    except Exception:
        pass

    return temp_ind







def link_wp(individual, all_routes, graph, start, end):
    return individual

def ex_segment(individual, all_routes, graph, start, end):
    return individual