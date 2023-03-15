import shortest_path_algorithms

routes_per_individual = 3
shortest_path_algo = shortest_path_algorithms.dijkstra

class individual():
    def __init__(self, graph, start, end) -> None:
        self.graph        = graph
        self.routes       = {n:shortest_path_algo(graph, start, end) for n in range(routes_per_individual)}
        self.edge_weights = {route:self.calculate_edge_weights(self.routes[route]) for route in self.routes}
        
    def calculate_edge_weights(self, route):
        route_edges = zip(route, route[1:])
        edge_weights = []
        for node_1, node_2 in route_edges:
            edge_weights.append(round(self.graph[node_1][node_2][0]['mean_travel_time'], 2))
            # TODO: apply a function that increases travel time as cars take the provided path
        return edge_weights


    def get_route_fitnesses(self):
        return {route:round(sum(self.edge_weights[route]), 2) for route in self.edge_weights}


    def get_overall_fitness(self):
        return round(sum(sum(self.edge_weights[route]) for route in self.edge_weights), 2)
