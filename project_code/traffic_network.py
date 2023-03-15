import copy

import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


class graph():

    def display_original(self):
        ax = self.df_geodata['geometry'].plot(color='#5a7d4d')
        nx.draw(self.graph, ax=ax, pos=self.zone_centroids, node_size=180, node_color='lightblue',
            linewidths=0.25, font_size=8, with_labels=True, arrowstyle='-')
        plt.show()
    
    # TODO: We may be able to see which method tends to be fastest by using timeit
    
    def display_shortest_path(self, start, end, method):
        ax = self.df_geodata['geometry'].plot(color='#5a7d4d')
        nx.draw(self.graph, ax=ax, pos=self.zone_centroids, node_size=180, node_color='lightblue',
            linewidths=0.25, font_size=8, with_labels=True, arrowstyle='-')
        # start: this code works but is temporary and purposely shows 3 different possible paths
        line_colors = ['red', 'blue', 'orange']
        paths_travel_times = []
        paths_routes = []
        for x in range(3):
            path_travel_time = 0
            shortest_path = method(start, end)
            path_edges    = set(zip(shortest_path, shortest_path[1:]))
            paths_routes.append(shortest_path)
            for n1, n2 in path_edges:
                print(f'{n1}->{n2}, weight = ' + str(self.graph[n1][n2][0]['mean_travel_time']))
                path_travel_time += self.graph[n1][n2][0]['mean_travel_time']
                # TODO: apply a function that increases travel time as cars take the provided path - simple version commented out below
                # rand_val = random.random()
                # self.graph[n1][n2][0]['mean_travel_time'] *= (3*rand_val)
                self.graph[n1][n2][0]['mean_travel_time'] *= 3
            paths_travel_times.append(path_travel_time)
            nx.draw_networkx_nodes(self.graph, pos=self.zone_centroids, nodelist=shortest_path, node_size=180, node_color=line_colors[x], alpha=0.6)
            nx.draw_networkx_edges(self.graph, pos=self.zone_centroids, edgelist=path_edges, edge_color=line_colors[x], alpha=0.6, arrowstyle='simple', width=0.25)
        print(f'Red Route    = {paths_routes[0]}')
        print(f'Red Route Travel Time    = {paths_travel_times[0]}')
        print(f'Blue Route   = {paths_routes[1]}')
        print(f'Blue Route Travel Time   = {paths_travel_times[1]}')
        print(f'Yellow Route = {paths_routes[2]}')
        print(f'Yellow Route Travel Time = {paths_travel_times[2]}')
        print(f'Total Travel Time        = {sum(paths_travel_times)}')
        # end of temp code
        plt.show()
