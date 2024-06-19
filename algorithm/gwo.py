import numpy as np
from utils import initialization
import sys
import pathlib

###########
# PATHING #
###########
CURR_FILE = pathlib.Path(__file__).resolve()
PROJECT_DIR = CURR_FILE.parents[2]

sys.path.append(PROJECT_DIR)


def GreyWolfOptimizer(search_agent, max_iter, lb, ub, dim, fobj):

    # initialize alpha, beta, delta
    alpha_pos = np.zeros(dim)
    alpha_score = float('inf')

    beta_pos = np.zeros(dim)
    beta_score = float('inf')

    delta_pos = np.zeros(dim)
    delta_score = float('inf')

    # initialize the position of search agents
    position = initialization(search_agent, dim, ub, lb)

    # convergence curve
    convergence_curve = np.zeros(max_iter).reshape(1,-1)

    l = 0 # loop counter

    while l < max_iter:
        # Check each agent/wolf fitness
        for i in range(position.shape[0]):
            # return back the search agent beyond the boundaries of search space
            flag4ub = position[i, :] > ub
            flag4lb = position[i, :] < lb
            position[i, :] = (position[i, :] * np.logical_not(flag4ub+flag4lb).astype(int)) + ub * flag4ub + lb * flag4lb

            fitness, route, distance = fobj(position[i, :].reshape(1,-1))

            # update alpha, beta, and delta
            if fitness < alpha_score:
                alpha_score = fitness # update alpha
                alpha_pos = position[i, :].reshape(1,-1)
                alpha_route = route

            if fitness > alpha_score and fitness < beta_score:
                beta_score = fitness
                beta_pos = position[i, :].reshape(1,-1)

            if fitness > alpha_score and fitness > beta_score and fitness < delta_score:
                delta_score = fitness
                delta_pos = position[i, :].reshape(1,-1)

        

        a = 2 - l * (2 / max_iter) # variable a decreases linearly fron 2 to 0

        # update the position of search agents including omega
        for i in range(position.shape[0]):
            for j in range(position.shape[1]):

                r1 = np.random.rand() # random number in [0,1]
                r2 = np.random.rand() # random number in [0,1]

                A1 = 2 * a * r1 - a # Equation (3.3)
                C1 = 2 * r2 # Equation (3.4)

                D_alpha = np.absolute(C1 * alpha_pos[:, j] - position[i, j]) # Equation (3.5)-part 1
                X1 = alpha_pos[:, j] - A1 * D_alpha # Equation (3.6)-part 1


                r1 = np.random.rand() # random number in [0,1]
                r2 = np.random.rand() # random number in [0,1]

                A2 = 2 * a * r1 - a # Equation (3.3)
                C2 = 2 * r2 # Equation (3.4)


                D_beta = np.absolute(C2 * beta_pos[:, j] - position[i, j]) # Equation (3.5)-part 2
                X2 = beta_pos[:, j] - A2 * D_beta # Equation (3.6)-part 2


                r1 = np.random.rand() # random number in [0,1]
                r2 = np.random.rand() # random number in [0,1]

                A3 = 2 * a * r1 - a # Equation (3.3)
                C3 = 2 * r2 # Equation (3.4)

                D_delta = np.absolute(C3 * delta_pos[:, j] - position[i, j]) # Equation (3.5)-part 3
                X3 = delta_pos[:, j] - A3 * D_delta # Equation (3.6)-part 3

                position[i, j] = (X1 + X2 + X3) / 3
                
        convergence_curve[:, l] = alpha_score
        l += 1
        

    return [alpha_score, alpha_pos, alpha_route, distance, convergence_curve]