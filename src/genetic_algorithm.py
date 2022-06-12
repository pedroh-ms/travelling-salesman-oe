import random
import numpy as np

from route import *


class GAModel:
    
    def __init__(self, lc_graph, start, num_generations, population_size, mutation_prob=0.3):
    
        self.distance_matrix = lc_graph.distance_matrix
        self.start = start
        self.num_generations = num_generations
        self.population_size = population_size
        self.mutation_prob = mutation_prob
        
    
    def run(self, initial_pop=None):
        
        if not initial_pop:
            population = [Route(self.start, self.start, self.distance_matrix) for i in range(self.population_size)]
        else:
            population = initial_pop
        
        self.best_route = population[0]
        for i in range(1, self.population_size):
            if population[i].cost < self.best_route.cost:
                self.best_route = population[i]
                    
        for g in range(self.num_generations):
                
            fitness_sum = 0    
            for i in range(self.population_size):
                fitness_sum += population[i].cost
        
            probability = []
            for i in range(self.population_size):
                probability.append((1 - (population[i].cost/fitness_sum)) / (self.population_size - 1))
                
            wheel = [probability[0]]
            for i in range(1, self.population_size):
                wheel.append(wheel[i - 1] + probability[i])
                
            selected = []
            n = len(wheel)
            for i in range(int(np.floor(self.population_size / 2))):
                p = random.random()
                for j in range(n):
                    if p < wheel[j]:
                        selected.append(population[j])
                        break
            
            population = []
            while selected != []:
                f, s = random.sample([k for k in range(len(selected))], 2)
                f_parent, s_parent = selected[f], selected[s]
                childs = Route.crossover(f_parent, s_parent)
                
                for child in childs:
                    p = random.random()
                    if p < self.mutation_prob:
                        child.mutate()
                        
                population += [f_parent, s_parent] + childs
                selected.remove(f_parent)
                selected.remove(s_parent)
            
            for i in range(self.population_size):
                if population[i].cost < self.best_route.cost:
                    self.best_route = population[i]                        
            

