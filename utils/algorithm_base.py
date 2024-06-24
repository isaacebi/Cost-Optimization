import numpy as np
from abc import ABC, abstractmethod

class Optimizer(ABC):
    def __init__(self, objective_func, dim, lb, ub, population_size, max_iter):
        self.objective_func = objective_func
        self.dim = dim
        self.lb = lb
        self.ub = ub
        self.population_size = population_size
        self.max_iter = max_iter
        self.convergence_curve = np.zeros(self.max_iter).reshape(1,-1)
        self.best_pos = None
        self.best_score = float('inf')
        

    @abstractmethod
    def optimize(self):
        pass

    def update_best_solution(self, pos, score, iteration):
        if score < self.best_score:
            self.best_score = score
            self.best_pos = pos.copy()
            self.convergence_curve[:, iteration] = score

    def initialization(self):
    
        # be sure to that ub, lb in 2d numpy array
        position = np.zeros((self.population_size, self.dim))

        boundary_no = self.ub.shape[1]

        # if boundary equall
        if boundary_no == 1:
            position = np.random.rand(self.population_size, self.dim) * (self.ub-self.lb) + self.lb

        if boundary_no > 1:
            for i in range(self.dim):
                ub_i = self.ub[:, i]
                lb_i = self.lb[:, i]
                position[:, i] = (np.random.rand(self.population_size, 1) * (ub_i-lb_i) + lb_i).reshape(1,-1)
        return position