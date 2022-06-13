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
            
            probability = [(1 - (population[i].cost/fitness_sum)) / (self.population_size - 1) for i in range(self.population_size)]
    
            wheel = [probability[0]]
            for i in range(1, self.population_size):
                wheel.append(wheel[i - 1] + probability[i])
                
            selected = [self.spinWheel(wheel, population) for i in range(int(np.floor(self.population_size / 2)))]
            
            new_population = []
            selected_len = len(selected)
            while selected != []:
                if selected_len != 1:
                    f, s = random.sample([k for k in range(len(selected))], 2)
                    f_parent, s_parent = selected[f], selected[s]
                    childs = Route.crossover(f_parent, s_parent)
                    selected.remove(f_parent)
                    selected.remove(s_parent)
                    
                    for child in childs:
                        p = random.random()
                        if p < self.mutation_prob:
                            child.mutate()
                            
                    new_population += [f_parent, s_parent] + childs                    
                else:
                    f_parent = selected[0]; s_parent = self.spinWheel(wheel, population)
                    childs = Route.crossover(f_parent, s_parent)
                    selected.remove(f_parent)
                    
                    i = random.randint(0, 1)
                    if random.random() < self.mutation_prob:
                        childs[i].mutate()
                        
                    new_population += [f_parent] + [childs[i]]
                             
                selected_len -= 2
            
            if len(new_population) < self.population_size:
                new_population += [self.spinWheel(wheel, population)]
            
            population = new_population
            
            for i in range(self.population_size):
                if population[i].cost < self.best_route.cost:
                    self.best_route = population[i]                        
            
    
    def spinWheel(self, wheel, population):
        p = random.random()
        for i in range(len(wheel)):
            if p < wheel[i]:
                return population[i]
            

