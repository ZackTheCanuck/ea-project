import geopandas as gpd
import networkx as nx
import pandas as pd


def build_graph():
    graph = nx.MultiDiGraph()

    # graph data
    df_geodata  = gpd.read_file('project_code/json_files/toronto_neighbourhoods.json')
    df_edges    = pd.read_csv('project_code/csv_files/toronto-neighbourhoods-2020-1-OnlyWeekdays-MonthlyAggregate.csv')
    
    # data filter values
    month_col    = 1
    weight_col   = 'mean_travel_time'
    zone_id_col  = 'MOVEMENT_ID'
    centroid_col = 'centroid'

    # add nodes to graph
    df_geodata[zone_id_col] = df_geodata[zone_id_col].astype(int)
    graph.add_nodes_from(df_geodata[zone_id_col])

    # add edges to graph
    df_geodata[centroid_col] = df_geodata.centroid
    df_geodata = df_geodata.set_geometry(centroid_col)

    # keep track of our edges to adjacent zones and the location of each zone's centroid
    neighbours_dict = {m_id: list(map(int, n.split(','))) for m_id, n in zip(df_geodata[zone_id_col], df_geodata['NEIGHBORS'])}
    zone_centroids  = {m_id: (c.x, c.y) for m_id, c in zip(df_geodata[zone_id_col], df_geodata[centroid_col])}

    nx.set_node_attributes(graph, zone_centroids, 'pos')

    filtered_edges = df_edges.loc[(df_edges['month'] == month_col)]
    weight_values = [(s, d, w) for s, d, w in zip(filtered_edges['sourceid'], filtered_edges['dstid'], filtered_edges[weight_col]) if (d in neighbours_dict[s])]

    graph.add_weighted_edges_from(weight_values, weight=weight_col)

    return graph
