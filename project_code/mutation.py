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

# instead of using capacity (which our data doesn't have), we take the sum of our fitnesses along each edge going out of each node,
# except the one we are currently using, and choose proportional to the fastest (lowest fitness) node
def link_wp(individual, all_unique_routes, graph, start, end):
    # Choose a random subset of routes proportional to their inverse traffic flow
    probabilities = ea_helpers.get_inverse_traffic_flow_probabilities(individual, all_unique_routes)
    # Select a random subset of route indices from all_unique_routes based on probabilities
    selected_routes_indices = np.random.choice(len(all_unique_routes), size=len(individual.routes) // 2, replace=False, p=probabilities)
    # Get the routes corresponding to the selected indices
    selected_routes = []
    for i in selected_routes_indices:
        selected_routes.append(all_unique_routes[i])
    for route in selected_routes:
        route_edges = list(zip(route, route[1:]))
        start_node_probs = []
        for i in range(len(route_edges)):
            node_out_edges = individual.graph.out_edges(route[i])
            outbound_travel_times = [individual.graph[edge[0]][edge[1]][0]['mean_travel_time'] for edge in node_out_edges if edge not in route_edges]
            start_node_probs.append(sum(outbound_travel_times))
        start_node_probs.append(0) # no point in starting at our goal node, so set the probability to 0
        percentages = [prob/sum(start_node_probs) for prob in start_node_probs]

        # Choose a start node and destination node
        route_length = len(route)
        # this hack lets us take the 2 indexes with the lowest outbound travel times
        non_selected_indexes = np.random.choice(route_length, route_length - 2, replace=False, p=percentages)
        selected_indexes = [i for i in range(route_length) if i not in non_selected_indexes]
        start_index  = min(selected_indexes)
        end_index    = max(selected_indexes)
        # Replace subsegment with a new random route
        new_subroute = shortest_path_algorithms.dijkstra(graph, route[start_index], route[end_index])
        new_route    = route[:start_index] + new_subroute[:-1] + route[end_index:]
        new_route    = ea_helpers.remove_cycles(new_route)
        individual.routes[individual.routes.index(route)] = new_route

    # Update all_unique_routes with new routes
    for route in individual.routes:
        if route not in all_unique_routes:
            all_unique_routes.append(route)

    return individual

def ex_segment(individual, all_routes, graph, start, end):
    return individual