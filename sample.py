import numpy as np
from algorithm import GreyWolfOptimizer
from objective_function import test_function

# simple sphere test function
f1 = test_function.Sphere()

# initiate standard data
[lb, ub, dim, fobj] = f1.get_data()

# using GWO to optimize
gwo = GreyWolfOptimizer(fobj, dim, lb, ub)
best_pos, best_score, converge_curve = gwo.optimize()

print(f"Best position: {best_pos}")
print(f"Best score: {best_score}")
print(f"Convergence curve: {converge_curve}")
print(len(converge_curve[0]))

