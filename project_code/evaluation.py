# evaluate fitness of a solution

def fitness(city_graph, route):
    route_edges = set(zip(route, route[1:]))
    travel_time = 0
    for node_1, node_2 in route_edges:
        travel_time += city_graph.get_edge_travel_time(node_1, node_2)
        # TODO: apply a function that increases travel time as cars take the provided path
    return round(travel_time, 2)