import os
import math
import random
import pathlib
import numpy as np
import matplotlib.pyplot as plt

###########
# PATHING #
###########
CURR_FILE = pathlib.Path(__file__).resolve()
PROJECT_DIR = CURR_FILE.parents[2]
RES = os.path.join(PROJECT_DIR, 'res')


#############
# FUNCTIONS #
#############
def plot_converge(gwo_curve, title, fname=None):
    x = np.arange(gwo_curve.shape[1])
    y = gwo_curve[0, :]
    plt.plot(x, y)
    plt.ylabel('Cost')
    plt.xlabel('Iteration')
    plt.title(title)

    if fname:
        plt.savefig(fname)
        
    plt.show()


def initialization(search_agent, dim, ub, lb):
  
    # be sure to that ub, lb in 2d numpy array
    position = np.zeros((search_agent, dim))

    boundary_no = ub.shape[1]

    # if boundary equall
    if boundary_no == 1:
        position = np.random.rand(search_agent, dim) * (ub-lb) + lb

    if boundary_no > 1:
        for i in range(dim):
            ub_i = ub[:, i]
            lb_i = lb[:, i]
            position[:, i] = (np.random.rand(search_agent, 1) * (ub_i-lb_i) + lb_i).reshape(1,-1)
    return position

# Euclidean distance
def get_distance(pointA, pointB):
    latA, longA = pointA
    latB, longB = pointB
    distance = 100 * math.sqrt((longB-longA)**2 + (latB-latA)**2)
    return distance


# Calculate fitness @ number of vehicle * distance
class Fitness:
    def __init__(self, customers, capacity, cost):
        self.customers = customers
        self.capacity = capacity
        self.cost = cost

    def get_fitness(self, route):
        actual_cost = 0
        distance = 0
        for i in range(len(route)-1):
            distance += get_distance(
                self.customers[self.customers['Customer']==route[i-1]].iloc[:, 1:3].values[0],
                self.customers[self.customers['Customer']==route[i]].iloc[:, 1:3].values[0]
            )
            cost = math.ceil(self.customers['Demand'].sum() / self.capacity) * float(self.cost)
            actual_cost += distance*cost

        return distance, actual_cost, cost
                
    def fitness_matrix(self, route):
        matrix = []
        for i in route:
            row_mat = []
            for j in route:
                distance = get_distance(
                    self.customers[self.customers['Customer']==i].iloc[:, 1:3].values[0],
                    self.customers[self.customers['Customer']==j].iloc[:, 1:3].values[0]
                )
                
                cost = math.ceil(self.customers['Demand'].sum() / self.capacity) * float(self.cost)                
                row_mat.append(distance*cost)
            matrix.append(row_mat)
        
        return matrix
    

class Generator_Route:
    def __init__(self, df):
        df['Depot_Distance'] = 0
        for idx, row in df.iterrows():
            depot_distance = get_distance(df.iloc[0, 1:3], [row['Latitude'], row['Longitude']])
            df['Depot_Distance'].loc[idx] = depot_distance   

        self.df = df

    def sorted_customer_id(self):
        list_customers = [0]
        list_customers += self.df.loc[1:].sort_values(['Customer'])['Customer'].to_list()
        list_customers += [0]
        return list_customers
    
    def sorted_lat_lon(self):
        list_customers = [0]
        list_customers += self.df.loc[1:].sort_values(['Latitude', 'Longitude'])['Customer'].to_list()
        list_customers += [0]
        return list_customers
    
    def sorted_depot(self):
        list_customers = [0]
        list_customers = self.df.loc[1:].sort_values(['Depot_Distance'])['Customer'].to_list()
        list_customers += [0]
        return list_customers
    
    def random(self):
        route = [0]
        list_customers = self.df.loc[1:]['Customer'].to_list()

        while list_customers:
            choice = random.choice(list_customers)
            route.append(choice)
            list_customers.remove(choice)

        route.append(0)

        return route
    

def find_nearest(array, value):
    array = np.asarray(array)
    array = array[~np.isnan(array)]
    idx = (np.abs(array - value)).argmin()
    return array[idx]