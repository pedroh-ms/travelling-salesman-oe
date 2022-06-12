import numpy as np
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import folium

from route import *
from simulated_annealing import *
from genetic_algorithm import *


class LocationGraph:

    def __init__(self, location, places, network_type):

        self.places = places

        # get the graph from the place specified in location with the type of
        # network_type
        self.g = ox.graph.graph_from_place(location, network_type=network_type)
        x, y = [], []

        # separate the coordinates in x, for longitude, and y, for latitude
        for k, v in self.places.items():
            x.append(v[0])
            y.append(v[1])

        # get the nearest nodes from the coordinates in the graph g
        self.node_ids = ox.distance.nearest_nodes(self.g, x, y)

        n = len(self.node_ids)
        # calculate the matrix distance from every place to every place
        self.distance_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                self.distance_matrix[i][j] = nx.shortest_path_length(G=self.g, 
                                                                     source=self.node_ids[i], 
                                                                     target=self.node_ids[j], 
                                                                     weight='length')
        
    def newRoute(self, source, target, from_places=None):

        return Route(source, target, self.distance_matrix, from_places)


    def travellingSalesman(self, start, method, **kwargs):
        
        if method == 'SA':
            model = SAModel(self, start, 
                            num_cycles=kwargs.get('num_cycles'),
                            num_att_per_cycle=kwargs.get('num_att_per_cycles'),
                            init_temp=kwargs.get('init_temp'))
                            
        if method == 'GA':
            model = GAModel(self, start,
                            num_generations=kwargs.get('num_generations'),
                            population_size=kwargs.get('population_size'),
                            mutation_prob=kwargs.get('mutation_prob'))

        return model


    def createRouteMap(self, otim_model):

        place_names = []
        coordinates = []
        for k, v in self.places.items():
            place_names.append(k)
            coordinates.append(v)
            
        path = []
        distances = []
        for i in range(len(otim_model.best_route.places) - 1):
            start_index = otim_model.best_route.places[i]
            end_index = otim_model.best_route.places[i + 1]
            
            source_node = ox.distance.nearest_nodes(self.g, 
                                                    coordinates[start_index][0], 
                                                    coordinates[start_index][1])
            target_node = ox.distance.nearest_nodes(self.g,
                                                    coordinates[end_index][0],
                                                    coordinates[end_index][1])

            path += nx.shortest_path(self.g, source_node, target_node, weight='length')[1:]
            distances.append(nx.shortest_path_length(G=self.g,
                                                     source=source_node,
                                                     target=target_node,
                                                     weight='length') / 1000)

        route_map = ox.folium.plot_route_folium(self.g, path, tiles='OpenStreetMap',
                                                tooltip=f'Total distance {np.sum(distances):0.2f} km')

        for i in range(len(otim_model.best_route.places) - 1):
            index = otim_model.best_route.places[i]
            folium.Marker((coordinates[index][1], coordinates[index][0]),
                          tooltip=f'{i}: {place_names[index]}; {distances[i]:0.2f} km to next place').add_to(route_map)
            folium.map.Marker(
                (coordinates[index][1], coordinates[index][0]),
                icon=folium.DivIcon(
                    icon_size=(250, 36),
                    icon_anchor=(0, 0),
                    html='<div style="font-size: 15pt">' + str(i) + '</div>',
                )
            ).add_to(route_map)

        return route_map

