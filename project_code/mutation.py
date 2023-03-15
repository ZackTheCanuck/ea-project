# mutation methods
import numpy as np
import shortest_path_algorithms


def calculate_traffic_flow(individual, all_routes):
    traffic_flow = []
    for unique_route in all_routes:
        flow_count = 0
        for route in individual.routes.values():
            if route == unique_route:
                flow_count += 1
        traffic_flow.append(flow_count)
    return traffic_flow

def get_inverse_traffic_flow_probabilities(individual, all_routes):
    traffic_flow = calculate_traffic_flow(individual, all_routes)
    total_flow = sum(traffic_flow)
    percentage_flows = [flow/total_flow for flow in traffic_flow]
    if 1.0 in percentage_flows:
        return percentage_flows
    inverse_flows = [1-pf if pf > 0 else 0 for pf in percentage_flows]
    percentage_inverse_flows = [invf/sum(inverse_flows) for invf in inverse_flows]
    return percentage_inverse_flows

# select a route to mutate inversely proportional to how often the route appears in the individual
# this makes sense because it assumes there is some reason we have evolved to generate a route multiple times,
# therefore it is more likely beneficial that we keep it
def new_route(individual, all_routes, graph, start, end):
    probabilities = get_inverse_traffic_flow_probabilities(individual, all_routes)
    all_routes_index = np.random.choice(range(len(all_routes)), p=probabilities)
    route_to_replace = all_routes[all_routes_index]
    
    route_index = list(individual.routes.keys())[list(individual.routes.values()).index(route_to_replace)]
    
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