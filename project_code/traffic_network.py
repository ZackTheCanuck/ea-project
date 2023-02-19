import random

import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


class graph():
    def __init__(self, geodata, edge_weights_csv, filter_parameter=1) -> None:
        self.df_geodata    = gpd.read_file(geodata)
        self.df_edges      = pd.read_csv(edge_weights_csv)
        self.graph         = nx.MultiDiGraph()
        self.filter        = filter_parameter

    # insert the nodes into the graph
    def add_graph_nodes(self, column='MOVEMENT_ID'):
        self.df_geodata[column] = self.df_geodata[column].astype(int)
        self.graph.add_nodes_from(self.df_geodata[column])

    # format the graph according to desired locations of nodes and edge values
    def format_graph(self, weights='mean_travel_time'):
        # extract the required fields to track neighbours and coordinates on map
        self.df_geodata['centroid'] = self.df_geodata.centroid
        self.df_geodata = self.df_geodata.set_geometry('centroid')

        # keep track of our edges to adjacent zones and the location of each zone's centroid
        self.neighbours_dict = {m_id: list(map(int, n.split(','))) for m_id, n in zip(self.df_geodata['MOVEMENT_ID'], self.df_geodata['NEIGHBORS'])}
        self.zone_centroids  = {m_id: (c.x, c.y) for m_id, c in zip(self.df_geodata['MOVEMENT_ID'], self.df_geodata['centroid'])}

        nx.set_node_attributes(self.graph, self.zone_centroids, 'pos')

        filtered_edges = self.df_edges.loc[(self.df_edges['month'] == self.filter)]
        weight_values = [(s, d, w) for s, d, w in zip(filtered_edges['sourceid'], filtered_edges['dstid'], filtered_edges[weights]) if (d in self.neighbours_dict[s])]

        self.graph.add_weighted_edges_from(weight_values, weight=weights)

    def build(self):
        self.add_graph_nodes()
        self.format_graph()
        print(self.graph)

    def display_original(self):
        ax = self.df_geodata['geometry'].plot(color='#5a7d4d')
        nx.draw(self.graph, ax=ax, pos=self.zone_centroids, node_size=180, node_color='lightblue',
            linewidths=0.25, font_size=8, with_labels=True, arrowstyle='-')
        plt.show()

    def get_nodes(self):
        return self.graph.nodes

    def get_neighbours(self):
        return self.neighbours_dict
    
    # TODO: We may be able to see which method tends to be fastest by using timeit
    def bellman_ford(self, start_node, end_node):
        print(f'Calculating shortest path from {start_node} -> {end_node} with Bellman-Ford\'s algorithm')
        path = nx.bellman_ford_path(G=self.graph, source=start_node, target=end_node, weight='mean_travel_time')
        return path
    
    def display_shortest_path(self, start, end, method):
        ax = self.df_geodata['geometry'].plot(color='#5a7d4d')
        nx.draw(self.graph, ax=ax, pos=self.zone_centroids, node_size=180, node_color='lightblue',
            linewidths=0.25, font_size=8, with_labels=True, arrowstyle='-')
        shortest_path = method(start, end)
        path_edges    = set((zip(shortest_path, shortest_path[1:])))
        nx.draw_networkx_nodes(self.graph, pos=self.zone_centroids, nodelist=shortest_path, node_size=180, node_color='r')
        nx.draw_networkx_edges(self.graph, pos=self.zone_centroids, edgelist=path_edges, edge_color='r', arrowstyle='simple', width=0.25)
        plt.show()


def main():
    json_geodata = 'project_code/json_files/toronto_neighbourhoods.json'
    neighbourhood_travel_times = 'project_code/csv_files/toronto-neighbourhoods-2020-1-OnlyWeekdays-MonthlyAggregate.csv'
    toronto_graph = graph(json_geodata, neighbourhood_travel_times, 1)
    toronto_graph.build()
    start, end = random.sample(list(toronto_graph.get_nodes()), 2)
    # toronto_graph.display_original()
    toronto_graph.display_shortest_path(start, end, toronto_graph.bellman_ford)


if __name__ == "__main__":
    main()