import random
import numpy as np


class Route:

    def __init__(self, source, target, distance_matrix, from_places=None):

        self.source = source
        self.target = target
        self.distance_matrix = distance_matrix

        if not from_places:
            n = self.distance_matrix.shape[0]
            if self.source == self.target:
                self.places = [self.source] + random.sample([i for i in range(n) if i != source and i != target], n - 1) + [self.target]
            else:
                self.places = [self.source] + random.sample([i for i in range(n) if i != source and i != target], n - 2) + [self.target]
        else:
            self.places = from_places

        self.calculateCost()


    def mutate(self):

        n = len(self.places)
        i, j = random.sample([k for k in range(1, n - 1)], 2)
        place_i = self.places[i]
        place_j = self.places[j]
        self.places[i] = place_j
        self.places[j] = place_i

        self.calculateCost()
        

    def calculateCost(self):

        self.cost = 0
        for i in range(1, len(self.places)):
            self.cost += self.distance_matrix[self.places[i - 1]][self.places[i]]
            
    @classmethod
    def crossover(cls, f_parent, s_parent):
        
        lf_parent = f_parent.places[1:-1]
        ls_parent = s_parent.places[1:-1]
        
        len_parent = len(lf_parent)
        n = int(np.floor(0.5 * float(len_parent)))
        f = random.randint(0, len_parent)
        
        lf_child = [None] * len_parent
        ls_child = [None] * len_parent
        
        for i in range(f, f + n):
            lf_child[i%len_parent] = lf_parent[i%len_parent]
            ls_child[i%len_parent] = ls_parent[i%len_parent]
        
        jf, js = f + n, f + n
        for i in range(f + n, len_parent + f + n):
            if lf_parent[i%len_parent] not in ls_child:
                ls_child[js%len_parent] = lf_parent[i%len_parent]
                js += 1
            if ls_parent[i%len_parent] not in lf_child:
                lf_child[jf%len_parent] = ls_parent[i%len_parent]
                jf += 1
            
        f_child = [f_parent.source] + lf_child + [f_parent.target]
        s_child = [s_parent.source] + ls_child + [s_parent.target]
            
        return [cls(f_parent.source, f_parent.target, f_parent.distance_matrix, f_child),
                cls(s_parent.source, s_parent.target, s_parent.distance_matrix, s_child)]
        
        
        
        
        

