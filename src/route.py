import random


class Route:

    def __init__(self, source, target, distance_matrix):

        self.source = source
        self.target = target
        self.distance_matrix = distance_matrix

        n = self.distance_matrix.shape[0]
        if source == target:
            self.places = [self.source] + random.sample([i for i in range(n) if i != source and i != target], n - 1) + [self.target]
        else:
            self.places = [self.source] + random.sample([i for i in range(n) if i != source and i != target], n - 2) + [self.target]

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

