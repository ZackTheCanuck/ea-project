import networkx as nx

# functions needed by multiple files

def calculate_traffic_flow(individual, all_routes):
    traffic_flow = []
    for unique_route in all_routes:
        flow_count = 0
        for route in individual.get_routes():
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

# find and remove cycles from a route
def remove_cycles(route):
    route_edges = list(zip(route, route[1:]))
    route_graph = nx.DiGraph(route_edges)
    cycles = list(nx.simple_cycles(route_graph))
    # if cycles:
    #     print(f'Cycles = {cycles}')
    for cycle in cycles:
        start, end = 0, len(cycle)
        while end < len(route):
            if route[start:end] == cycle:
                del route[start:end]
            else:
                start += 1
                end += 1
    return route