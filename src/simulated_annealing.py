import random
import numpy as np
from copy import deepcopy

from route import *


class SAModel:
    '''Simulated annealing model to solve the travelling salesman problem.
    
    :param lc_graph: The :class:`location_graph.LocationGraph` object of the location
    :type lc_graph: class:`location_graph.LocationGraph`
    :param start: The start place of the problem
    :type start: int
    :param num_cycles: Number of cycles
    :type num_cycles: int
    :param num_att_per_cycle: Number of attempts per cycle
    :type num_att_per_cycle: int
    :param init_temp: Initial temperature, defaults to 200
    :type init_temp: int, optional
    '''

    def __init__(self, lc_graph, start, num_cycles, num_att_per_cycle, init_temp=200):
        '''Constructor method of SAModel.
        '''
        self.distance_matrix = lc_graph.distance_matrix
        self.start = start
        self.num_cycles = num_cycles
        self.num_att_per_cycle = num_att_per_cycle
        self.init_temp = init_temp
        

    def run(self, initial_route=None):
        '''Runs the metaheuristic.
        
        :param initial_route: Initial route to start the metaheuristic, defaults to None
        :type initial_route: class:`route.Route`, optional
        '''
        if not initial_route: # generates the first route randomly or assign initial_route to self.best_route
            self.best_route = Route(self.start, self.start, self.distance_matrix)
        else:
            self.best_route = initial_route


        t = self.init_temp
        na = 1.0
        delta_energ_avg = 0.0
        for i in range(self.num_cycles):
            for j in range(self.num_att_per_cycle):
                
                # copies the current solution and mutate it
                new_route = deepcopy(self.best_route)
                new_route.mutate()
                
                # calculates the variation of energy
                delta_energ = abs(new_route.cost - self.best_route.cost)
                
                # tests if the new route is worst than the current route
                # accepts the new route if not
                if new_route.cost > self.best_route.cost:

                    if i==0 and j==0: delta_energ_avg = delta_energ

                    # calculates the probability of acceptance
                    if random.random() < np.exp(-delta_energ/(delta_energ_avg * t)):
                        accept_change = True
                    else:
                        accept_change = False

                else:
                    accept_change = True
                
                if accept_change:
                   self.best_route = new_route
                   na += 1.0
                   delta_energ_avg = (delta_energ_avg * (na - 1.0) + delta_energ) / na

            t = ((i + 1) / self.num_cycles) * t # reduces temperature

