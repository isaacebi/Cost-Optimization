import sys
import pathlib
import numpy as np
from utils.algorithm_base import Optimizer


class GreyWolfOptimizer(Optimizer):
    def __init__(self, objective_func, dim, lb, ub, num_wolves=10, max_iter=100):
        super().__init__(objective_func, dim, lb, ub, num_wolves, max_iter)
        self.alpha_pos = np.zeros(self.dim)
        self.alpha_score = float('inf')
        
        self.beta_pos = np.zeros(self.dim)
        self.beta_score = float('inf')
        
        self.delta_pos = np.zeros(self.dim)
        self.delta_score = float('inf')

        self.positions = self.initialization()


    def update_wolf_hierarchy(self, fitness, j, i):
        # alpha
        if fitness < self.beta_score:
            self.alpha_score = fitness
            self.alpha_pos = self.positions[j].copy()

        elif fitness < self.alpha_score & fitness > self.delta_score:
            self.beta_score = fitness
            self.beta_pos = self.positions[j].copy()

        elif fitness < self.delta_score:
            self.delta_score = fitness
            self.delta_pos = self.positions[j].copy()

        super().update_best_solution(self.positions[j], fitness, i)


    def update_wolf_positions(self, a):
        # update each wolf
        for j in range(self.population_size):
            for k in range(self.dim):
                X1 = self.calculate_new_position(self.alpha_pos[k], self.positions[j, k], a)
                X2 = self.calculate_new_position(self.beta_pos[k], self.positions[j, k], a)
                X3 = self.calculate_new_position(self.delta_pos[k], self.positions[j, k], a)
                
                self.positions[j, k] = (X1 + X2 + X3) / 3
                # return each agent to edges of search spaces
                self.positions[j, k] = np.clip(self.positions[j, k], self.lb, self.ub)

    def calculate_new_position(self, leader_pos, wolf_pos, a):
        r1, r2 = np.random.random(2)
        A = 2 * a * r1 - a
        C = 2 * r2
        D = abs(C * leader_pos - wolf_pos)
        return leader_pos - A * D
    
    def optimize(self):
        for i in range(self.max_iter):
            for j in range(self.population_size):
                # fitness
                fitness = self.objective_func(self.positions[j])
                self.update_wolf_hierarchy(fitness, j, i)
            
            a = 2 - i * (2 / self.max_iter)
            self.update_wolf_positions(a)

        self.best_pos = self.alpha_pos
        self.best_score = self.alpha_score
        return self.best_pos, self.best_score, self.convergence_curve
