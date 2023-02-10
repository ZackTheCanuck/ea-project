from collections import defaultdict

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
        ids_list, neighbours_list, centroid_list = self.df_geodata['MOVEMENT_ID'].to_list(), self.df_geodata['NEIGHBORS'].to_list(), self.df_geodata['centroid'].to_list()

        # keep track of our edges to adjacent zones and the location of each zone's centroid
        self.neighbours_dict = defaultdict(list)
        self.zone_centroids  = {}
        for id_num, neighbours, centroid in zip(ids_list, neighbours_list, centroid_list):
            self.zone_centroids[int(id_num)] = (centroid.x, centroid.y)
            ids_neighbours = list(map(int, neighbours.split(',')))
            for neighbour in ids_neighbours:
                self.neighbours_dict[id_num].append(neighbour)
        nx.set_node_attributes(self.graph, self.zone_centroids, 'pos')

        # extract the required fields to insert edges into graph
        sources, destinations, travel_times, filter_by = self.df_edges['sourceid'].to_list(), self.df_edges['dstid'].to_list(), self.df_edges[weights].to_list(), self.df_edges['month'].to_list()
        weight_values = []
        for s, d, t, f in zip(sources, destinations, travel_times, filter_by):
            if (int(f) == self.filter) and (d in self.neighbours_dict[s]):
                edge_info = (s, d, t)
                weight_values.append(edge_info)
        self.graph.add_weighted_edges_from(weight_values, weight=weights)

    def build(self):
        self.add_graph_nodes()
        self.format_graph()
        print(self.graph)

    def display(self):
        ax = self.df_geodata['geometry'].plot(color='#5a7d4d')
        nx.draw(self.graph, ax=ax, pos=self.zone_centroids, node_size=180, node_color='lightblue',
            linewidths=0.25, font_size=8, with_labels=True, arrowstyle='-')
        plt.show()

    def get_neighbours(self):
        return self.neighbours_dict


def main():
    json_geodata = 'project_code/json_files/toronto_neighbourhoods.json'
    neighbourhood_travel_times = 'project_code/csv_files/toronto-neighbourhoods-2020-1-OnlyWeekdays-MonthlyAggregate.csv'
    toronto_graph = graph(json_geodata, neighbourhood_travel_times, 1)
    toronto_graph.build()
    toronto_neighbours = toronto_graph.get_neighbours()
    print(toronto_neighbours)
    toronto_graph.display()


if __name__ == "__main__":
    main()