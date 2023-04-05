import copy

import networkx as nx
import numpy as np


# this gives us near-optimal routing, our (simplified) version of randDijkstra
def create_edge_variance(graph):
    graph_copy = copy.deepcopy(graph)
    for _, _, edge_weight in graph_copy.edges(data=True):
        edge_weight['mean_travel_time'] = round(abs(np.random.normal((edge_weight['mean_travel_time']), 0.8 * edge_weight['mean_travel_time'])), 2)
    return graph_copy


def bellman_ford(graph, start_node, end_node):
    path = nx.bellman_ford_path(G=graph, source=start_node, target=end_node, weight='mean_travel_time')
    return path

def dijkstra(graph, start_node, end_node):
    path = nx.dijkstra_path(G=graph, source=start_node, target=end_node, weight='mean_travel_time')
    return path

def floyd_warshall(graph, start_node, end_node):
    predecessors, _ = nx.floyd_warshall_predecessor_and_distance(G=graph, weight='mean_travel_time')
    path = nx.reconstruct_path(start_node, end_node, predecessors)
    return path

def a_star(graph, start_node, end_node):
    path = nx.astar_path(G=graph, source=start_node, target=end_node, weight='mean_travel_time')
    return path

def bellman_ford_variance(graph, start_node, end_node):
    edge_variance_graph = create_edge_variance(graph)
    path = nx.bellman_ford_path(G=edge_variance_graph, source=start_node, target=end_node, weight='mean_travel_time')
    return path

def dijkstra_variance(graph, start_node, end_node):
    edge_variance_graph = create_edge_variance(graph)
    path = nx.dijkstra_path(G=edge_variance_graph, source=start_node, target=end_node, weight='mean_travel_time')
    return path

def floyd_warshall_variance(graph, start_node, end_node):
    edge_variance_graph = create_edge_variance(graph)
    predecessors, _ = nx.floyd_warshall_predecessor_and_distance(G=edge_variance_graph, weight='mean_travel_time')
    path = nx.reconstruct_path(start_node, end_node, predecessors)
    return path

def a_star_variance(graph, start_node, end_node):
    edge_variance_graph = create_edge_variance(graph)
    path = nx.astar_path(G=edge_variance_graph, source=start_node, target=end_node, weight='mean_travel_time')
    return path