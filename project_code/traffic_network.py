from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

import os


class graph():
    def __init__(self, neighbours_csv, edge_weights_csv, filter_parameter=1) -> None:
        self.df_neighbours = pd.read_csv(neighbours_csv)
        self.df_edges      = pd.read_csv(edge_weights_csv)
        self.graph         = nx.MultiDiGraph()
        self.filter        = filter_parameter

    # insert the nodes into the graph
    def add_graph_nodes(self, column='MOVEMENT_ID'):
        self.graph.add_nodes_from(self.df_neighbours[column])

    # insert the edges into the graph
    def add_graph_edges(self, weights='mean_travel_time'):
        # extract the required fields to track neighbours
        ids_list, neighbours_list = self.df_neighbours['MOVEMENT_ID'].to_list(), self.df_neighbours['NEIGHBORS'].to_list()

        # keep track of our edges to adjacent zones
        self.neighbours_dict = defaultdict(list)
        for id_num, neighbours in zip(ids_list, neighbours_list):
            ids_neighbours = list(map(int, neighbours.split(',')))
            for neighbour in ids_neighbours:
                self.neighbours_dict[id_num].append(neighbour)

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
        self.add_graph_edges()
        print(self.graph)

    def display(self):
        nx.draw(self.graph, pos=nx.nx_agraph.graphviz_layout(self.graph), node_size=200, node_color='lightblue',
            linewidths=0.25, font_size=8, with_labels=True, arrowstyle='-')
        plt.show()

    def get_neighbours(self):
        return self.neighbours_dict
    

def main():
    neighbourhood_neighbours   = 'project_code/csv_files/toronto_neighbourhood_neighbours.csv'
    neighbourhood_travel_times = 'project_code/csv_files/toronto-neighbourhoods-2020-1-OnlyWeekdays-MonthlyAggregate.csv'
    toronto_graph = graph(neighbourhood_neighbours, neighbourhood_travel_times, 1)
    toronto_graph.build()
    toronto_neighbours = toronto_graph.get_neighbours()
    print(toronto_neighbours)
    toronto_graph.display()


if __name__ == "__main__":
    main()