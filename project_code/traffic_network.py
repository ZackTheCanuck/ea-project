from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


# insert the nodes into the graph
def add_nodes(zones_dataframe):
    
    graph = nx.MultiDiGraph()
    graph.add_nodes_from(zones_dataframe['MOVEMENT_ID'])

    return graph


# insert the edges into the graph, this is a separate function since we can have different weights for different times, days, months, etc
def add_edges(graph, neighbours_dataframe, edges_dataframe, month):

    id_list          = neighbours_dataframe['MOVEMENT_ID'].to_list()
    neighbours_frame = neighbours_dataframe['NEIGHBORS'].to_list()

    # keep track of our edges to adjacent zones
    neighbours_dict = defaultdict(list)
    for id_num, neighbours in zip(id_list, neighbours_frame):
        ids_neighbours = list(map(int, neighbours.split(',')))
        for neighbour in ids_neighbours:
            neighbours_dict[id_num].append(neighbour)

    sources      = edges_dataframe['sourceid'].to_list()
    destinations = edges_dataframe['dstid'].to_list()
    travel_times = edges_dataframe['mean_travel_time'].to_list()
    months       = edges_dataframe['month'].to_list()

    weight_values = []
    for s, d, t, m in zip(sources, destinations, travel_times, months):
        if (int(m) == month) and (d in neighbours_dict[s]):
            edge_info = (s, d, t)
            weight_values.append(edge_info)
    graph.add_weighted_edges_from(weight_values, weight='mean_travel_time')
    # print(graph.get_edge_data(107, 1))
    # print(graph.edges.data())

    return graph, neighbours_dict


# build our NetworkX graph
def build_graph(neighbours_csv, edge_weights_csv, month):
    
    df_neighbours = pd.read_csv(neighbours_csv)
    df_edges = pd.read_csv(edge_weights_csv)

    toronto_graph = add_nodes(df_neighbours)
    toronto_graph, neigbours_dict = add_edges(toronto_graph, df_neighbours, df_edges, month)
    
    return toronto_graph, neigbours_dict


# use matplotlib to display a graph
def display_graph(graph):

    nx.draw(graph, pos=nx.nx_agraph.graphviz_layout(graph), node_size=200, node_color='lightblue',
            linewidths=0.25, font_size=8, with_labels=True, arrowstyle='-')
    # labels = nx.get_edge_attributes(graph,'mean_travel_time')
    # nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()


def main():
    
    toronto_graph, neigbours_dict = build_graph('toronto_neighbourhood_neighbours.csv', 'toronto-neighbourhoods-2020-1-OnlyWeekdays-MonthlyAggregate.csv', 1)
    print(toronto_graph)
    # print(neigbours_dict)
    # display_graph(toronto_graph)


if __name__ == "__main__":
    main()