import numpy as np
from abc import ABC, abstractmethod

class Test_Function(ABC):
    def __init__(self, dim, lb, ub):
        self.dim = dim
        self.lb = np.array(lb, ndmin=2)
        self.ub = np.array(ub, ndmin=2)

    @abstractmethod
    def get_score(self):
        pass

    def get_data(self):
        return [self.lb, self.ub, self.dim, self.get_score]