from collections import Counter
from itertools import chain

import matplotlib.pyplot as plt
import networkx as nx
import shortest_path_algorithms
from matplotlib import colors as mcolors

routes_per_individual = 3
shortest_path_algo = shortest_path_algorithms.dijkstra

class individual():
    def __init__(self, graph, start, end) -> None:
        self.graph        = graph
        self.routes       = [shortest_path_algo(graph, start, end) for _ in range(routes_per_individual)]
        self.edge_weights = [self.get_edge_weights(route) for route in self.routes]
        
    def get_edge_weights(self, route):
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
    
    def display(self, geodata):
        ax = geodata['geometry'].plot(color='#5a7d4d')
        zone_centroids  = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, ax=ax, pos=zone_centroids, node_size=180, node_color='lightblue',
            linewidths=0.25, font_size=8, with_labels=True, arrowstyle='-')
        # mcolors.TABLEAU_COLORS supports up to 10 routes for us
        line_colors = list(mcolors.TABLEAU_COLORS)
        for i, route in enumerate(self.routes):
            path_edges = list(zip(route, route[1:]))
            nx.draw_networkx_nodes(self.graph, pos=zone_centroids, nodelist=route, node_size=180, node_color=line_colors[i], alpha=0.6)
            nx.draw_networkx_edges(self.graph, pos=zone_centroids, edgelist=path_edges, edge_color=line_colors[i], alpha=0.6, arrowstyle='simple', width=0.25)
        plt.show()
    
    def __str__(self):
        return f"Individual object with routes: {self.routes}"
