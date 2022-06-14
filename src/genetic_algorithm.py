import random
import numpy as np

from route import *


class GAModel:
    '''Genetic algorithm model to solve the travelling salesman problem.
    
    :param lc_graph: The :class:`location_graph.LocationGraph` object of the location
    :type lc_graph: class:`location_graph.LocationGraph`
    :param start: The start place of the problem
    :type start: int
    :param num_generations: Number of generations
    :type num_generations: int
    :param population_size: Size of the population
    :type population_size: int
    :param mutation_prob: Probability of mutation, defaults to 0.3
    :type mutation_prob: float, optional'''
    
    def __init__(self, lc_graph, start, num_generations, population_size, mutation_prob=0.3):
        '''Constructor method of GAModel.
        '''
        self.distance_matrix = lc_graph.distance_matrix
        self.start = start
        self.num_generations = num_generations
        self.population_size = population_size
        self.mutation_prob = mutation_prob
        
    
    def run(self, initial_pop=None):
        '''Run the metaheuristic.
        
        :param initial_pop: Initial population to start the metaheuristic, defaults to None
        :type initial_pop: list
        '''
        if not initial_pop: # randomly generates the first population or assign initial_pop to population
            population = [Route(self.start, self.start, self.distance_matrix) for i in range(self.population_size)]
        else:
            population = initial_pop
        
        # searches for the individual with the best solution
        self.best_route = population[0]
        for i in range(1, self.population_size):
            if population[i].cost < self.best_route.cost:
                self.best_route = population[i]
                    
        for g in range(self.num_generations):
            
            # calculates the total fitness    
            fitness_sum = 0    
            for i in range(self.population_size):
                fitness_sum += population[i].cost
            
            # calculates the probability of each individual
            probability = [(1 - (population[i].cost/fitness_sum)) / (self.population_size - 1) for i in range(self.population_size)]
            
            # calculates the accumulated probabilities of the fitness proportionate selection
            # or the wheel of the roulette wheel selection
            wheel = [probability[0]]
            for i in range(1, self.population_size):
                wheel.append(wheel[i - 1] + probability[i])
            
            # selects half of the population for crossover    
            selected = [self.spinWheel(wheel, population) for i in range(int(np.floor(self.population_size / 2)))]
            
            new_population = []
            selected_len = len(selected)
            while selected != []: # makes the crossover of the selected individuals
                if selected_len != 1: 
                    # randomly selects two indexes
                    f, s = random.sample([k for k in range(len(selected))], 2)
                    f_parent, s_parent = selected[f], selected[s]
                    childs = Route.crossover(f_parent, s_parent) # makes the crossover
                    # removes the parents from the list of selected individuals
                    selected.remove(f_parent)
                    selected.remove(s_parent)
                    
                    for child in childs: # randomly mutates the children
                        p = random.random()
                        if p < self.mutation_prob:
                            child.mutate()
                            
                    new_population += [f_parent, s_parent] + childs                    
                else: # for the cases when the length of the list of selected individuals is odd
                
                    # gets the last selected individual and select other
                    f_parent = selected[0]; s_parent = self.spinWheel(wheel, population)
                    childs = Route.crossover(f_parent, s_parent) # makes the crossover
                    # removes the last selected individual
                    selected.remove(f_parent)
                    
                    # randomly selects and mutates one child
                    i = random.randint(0, 1)
                    if random.random() < self.mutation_prob:
                        childs[i].mutate()
                        
                    new_population += [f_parent] + [childs[i]]
                             
                selected_len -= 2
            
            # for the cases when the length of the population list is odd
            if len(new_population) < self.population_size:
                new_population += [self.spinWheel(wheel, population)]
            
            population = new_population
            
            # searches for the individual with the best solution
            for i in range(self.population_size):
                if population[i].cost < self.best_route.cost:
                    self.best_route = population[i]                        
            
    
    def spinWheel(self, wheel, population):
        '''Method for fitness proportionate selection or roulette wheel selection.
        
        :param wheel: List containing the acumulated probabilities
        :type wheel: list
        :param population: List containing all the individuals of the population
        :type population: list
        :return: The selected individual
        :rtype: class:`route.Route`
        '''
        p = random.random()
        for i in range(self.population_size):
            if p < wheel[i]:
                return population[i]
            

