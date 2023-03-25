from collections import Counter
from itertools import chain

import shortest_path_algorithms

routes_per_individual = 3
shortest_path_algo = shortest_path_algorithms.dijkstra

class individual():
    def __init__(self, graph, start, end) -> None:
        self.graph        = graph
        self.routes       = [shortest_path_algo(graph, start, end) for _ in range(routes_per_individual)]
        self.edge_weights = [self.calculate_edge_weights(route) for route in self.routes]
        
    def calculate_edge_weights(self, route):
        route_edges = zip(route, route[1:])
        edge_weights = []
        for node_1, node_2 in route_edges:
            edge_weights.append(round(self.graph[node_1][node_2][0]['mean_travel_time'], 2))
        return edge_weights

    # def get_route_fitnesses(self, route):
    #     return {route:round(sum(edge_weights[route]), 2) for route in self.edge_weights}

    def get_overall_fitness(self):
        all_route_edges    = [zip(route, route[1:]) for route in self.routes]
        all_edges_combined = list(chain.from_iterable(all_route_edges))
        edge_flows         = Counter(all_edges_combined)
        edge_travel_times  = [self.graph[edge[0]][edge[1]][0]['mean_travel_time'] * edge_flows[edge] for edge in all_edges_combined]
        overall_fitness    = sum(edge_travel_times)
        return round(overall_fitness, 2)
    
    def get_routes(self):
        return self.routes[:]
