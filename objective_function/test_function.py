import numpy as np
from utils import Test_Function

# simple sphere formula
class Sphere(Test_Function):
    def __init__(self, dim=30, lb=-100, ub=100):
        self.dim = dim
        self.lb = np.ones_like([np.arange(dim)]) * lb
        self.ub = np.ones_like([np.arange(dim)]) * ub

    def get_score(self, x):
        return np.sum(x**2)
