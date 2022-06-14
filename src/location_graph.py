import numpy as np
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import folium

from route import *
from simulated_annealing import *
from genetic_algorithm import *


class LocationGraph:
    '''LocationGraph class that represents the location where the places are
    as a graph.
    
    :param location: The name of the location
    :type location: str
    :param places: Dictionary containing the coordinates of the places
    :type places: dict
    :param network_type: The type of the graph
    :type network_type: str
    '''

    def __init__(self, location, places, network_type):
        '''Constructor method of LocationGraph.
        '''
        self.places = places

        # gets the graph from the place specified in location with the type of
        # network_type
        self.g = ox.graph.graph_from_place(location, network_type=network_type)
        x, y = [], []

        # separates the coordinates in x, for longitude, and y, for latitude
        for k, v in self.places.items():
            x.append(v[0])
            y.append(v[1])

        # gets the nearest nodes from the coordinates in the graph g
        self.node_ids = ox.distance.nearest_nodes(self.g, x, y)

        n = len(self.node_ids)
        # calculates the matrix distance from every place to every place
        self.distance_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                self.distance_matrix[i][j] = nx.shortest_path_length(G=self.g, 
                                                                     source=self.node_ids[i], 
                                                                     target=self.node_ids[j], 
                                                                     weight='length')
        
    def newRoute(self, source, target, from_places=None):
        '''Creates a new route based on the location graph.
        
        :param source: The source place of the route
        :type source: int
        :param target: The target place of the route
        :type target: int
        :param from_places: A list that defines the places of the route, defaults to None
        :type from_places: list, optional
        :return: A :class:`route.Route` object
        :rtype: class: `route.Route`
        '''
        return Route(source, target, self.distance_matrix, from_places)


    def travellingSalesman(self, start, method, **kwargs):
        '''Method for the travelling salesman problem solved with metaheuristics.
        
        :param start: The start place of the problem
        :type start: int
        :param method: The metaheuristics to solve the problem
        :type method: str
        :param `**kwargs`: Keyword arguments to pass different values to the arguments of the metaheuristics
        :return: A model class of the metaheuristic defined in method
        :rtype: class:`simulated_annealing.SAModel` or class:`genetic_algorithm.GAModel`
        '''
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
        '''Creates the route map of the best solution of the travelling salesman problem.
        
        :param otim_model: Model used to find the best solution
        :type otim_model: class:`simulated_annealing.SAModel` or class:`genetic_algorithm.GAModel`
        :return: The map object of the best route
        :rtype: class:`folium.folium.map`
        '''
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

