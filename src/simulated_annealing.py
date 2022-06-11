import random
import numpy as np
from copy import deepcopy

from route import *


class SAModel:

    def __init__(self, lc_graph, start, num_cycles, num_att_per_cycle, init_temp=200):

        self.distance_matrix = lc_graph.distance_matrix
        self.start = start
        self.num_cycles = num_cycles
        self.num_att_per_cycle = num_att_per_cycle
        self.init_temp = init_temp

    def solve(self, initial_route=None):

        if not initial_route:
            self.best_route = Route(self.start, self.start, self.distance_matrix)
        else:
            self.best_route = initial_route


        t = self.init_temp
        na = 1.0
        delta_energ_avg = 0.0
        for i in range(self.num_cycles):
            for j in range(self.num_att_per_cycle):

                new_route = deepcopy(self.best_route)
                new_route.mutate()

                delta_energ = abs(new_route.cost - self.best_route.cost)

                if new_route.cost > self.best_route.cost:

                    if i==0 and j==0: delta_energ_avg = delta_energ

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

            t = ((i + 1) / self.num_cycles) * t 
                   
