import os
import math
import pathlib
import numpy as np
import pandas as pd
import sys

from utils import Fitness, Generator_Route, find_nearest


###########
# PATHING #
###########
CURR_FILE = pathlib.Path(__file__).resolve()
PROJECT_DIR = CURR_FILE.parents[2]
VEHICLE = os.path.join(os.getcwd(), 'data', 'vehicle.csv')
CUSTOMERS = os.path.join(os.getcwd(), 'data', 'customer.csv')

sys.path.append(PROJECT_DIR)



#############
# VARIABLES #
#############

# depot coordinate
DEPOT = pd.DataFrame({
    'Customer': 0,
    'Latitude': 4.4184,
    'Longitude': 114.0932,
    'Demand': 0
}, index=[0])

# reading file
customers = pd.read_csv(CUSTOMERS)
vehicle = pd.read_csv(VEHICLE)

# cleaning variable
vehicle['Cost'] = vehicle['Cost'].str.replace('RM', "").str.replace('per km', "")

# combining customer with depot
customers = pd.concat([DEPOT, customers]).reset_index(drop=True)

def get_function(F):
    num_cust = len(customers.loc[1:])
    search_spaces = customers['Customer'].loc[1:].to_list()

    ######################
    # Objective function #
    ######################

    # https://en.wikipedia.org/wiki/2-opt
    def Two_Opt(x):
        fit_obj = Fitness(
            customers=customers,
            capacity=vehicle['Capacity'].loc[round(x[0][0])],
            cost=vehicle['Cost'].loc[round(x[0][0])]
        )
        generator = Generator_Route(customers)

        try:
            sel_gen_route = round(x[0][1])
        except IndexError:
            sel_gen_route = math.floor(x[0][1])

        if sel_gen_route == 0:
            route = generator.sorted_customer_id()
        if sel_gen_route == 1:
            route = generator.sorted_lat_lon()
        if sel_gen_route == 2:
            route = generator.sorted_depot()
        if sel_gen_route == 3:
            route = generator.random()


        if route:
            v1 = round(x[0][2])
            a = route[1:v1]

            if x[0][2] < x[0][3]:
                v2 = v1+1
            else:
                v2 = round(x[0][3])            
            b = list(reversed(route[v1:v2]))

            c = route[v2:-1]
            new_route = [route[0]] +a+b+c + [route[0]]

        distance, actual_cost, cost = fit_obj.get_fitness(new_route)
        return [actual_cost, route, distance]


    # Greedy Method
    # Not simulated, too long to compute with limited time constrains.
    def Greedy(x):
        fit_obj = Fitness(
            customers=customer,
            capacity=vehicle['Capacity'].loc[round(x[0][0])],
            cost=vehicle['Cost'].loc[round(x[0][0])]
        )
        generator = Generator_Route(customers)
        depot_space = generator.sorted_depot()

        route = []
        # set direction
        for customer in x[0]:
            selector = round(customer)
            if depot_space[selector] == np.nan:
                route.append(
                    find_nearest(depot_space, round(selector))
                )
    
            route.append(depot_space[selector])
            depot_space[selector] = np.nan


        distance, actual_cost, cost = fit_obj.get_fitness(route)
        return [actual_cost, route, distance]
    
    # https://en.wikipedia.org/wiki/2-opt
    def Swap_TypeA(x):
        typeA = Fitness(
            customers=customers,
            capacity=vehicle['Capacity'].loc[0],
            cost=vehicle['Cost'].loc[0]
        )
        generator = Generator_Route(customers)

        try:
            sel_gen_route = round(x[0][0])
        except IndexError:
            sel_gen_route = math.floor(x[0][0])

        if sel_gen_route == 0:
            route = generator.sorted_customer_id()
        if sel_gen_route == 1:
            route = generator.sorted_lat_lon()
        if sel_gen_route == 2:
            route = generator.sorted_depot()
        if sel_gen_route == 3:
            route = generator.random()

        if route:
            v1 = round(x[0][1])
            a = route[1:v1]

            if x[0][2] < x[0][1]:
                v2 = v1+1
            else:
                v2 = round(x[0][2])            
            b = list(reversed(route[round(x[0][1]):v2]))

            c = route[round(x[0][2]):-1]
            new_route = [route[0]] +a+b+c + [route[0]]

        distance, actual_cost, cost = typeA.get_fitness(new_route)
        return [actual_cost, route, distance]

    # https://en.wikipedia.org/wiki/2-opt
    def Swap_TypeB(x):
        typeA = Fitness(
            customers=customers,
            capacity=vehicle['Capacity'].loc[1],
            cost=vehicle['Cost'].loc[1]
        )
        generator = Generator_Route(customers)

        try:
            sel_gen_route = round(x[0][0])
        except IndexError:
            sel_gen_route = math.floor(x[0][0])

        if sel_gen_route == 0:
            route = generator.sorted_customer_id()
        if sel_gen_route == 1:
            route = generator.sorted_lat_lon()
        if sel_gen_route == 2:
            route = generator.sorted_depot()
        if sel_gen_route == 3:
            route = generator.random()

        if route:
            v1 = round(x[0][1])
            a = route[1:v1]

            if x[0][2] < x[0][1]:
                v2 = v1+1
            else:
                v2 = round(x[0][2])            
            b = list(reversed(route[round(x[0][1]):v2]))

            c = route[round(x[0][2]):-1]
            new_route = [route[0]] +a+b+c + [route[0]]

        distance, actual_cost, cost = typeA.get_fitness(new_route)
        return [actual_cost, route, distance]
    

    # selection function
    if F == "Two_Opt":
        fobj = Two_Opt
        lb = np.zeros([1, 4])
        ub_swap = np.ones([1, 2]) * num_cust
        ub_gen_route = np.array([[3]])
        ub_vech = np.ones([1, 1])
        ub = np.hstack([ub_vech, ub_gen_route, ub_swap])
        dim = lb.shape[1]
        return [lb, ub, dim, fobj]
    
    if F == "Greedy":
        fobj = Greedy
        lb = np.zeros([1, num_cust+1])
        ub_cus = np.ones([1, num_cust]) * num_cust
        ub_vech = np.ones([1, 1])
        ub = np.hstack([ub_vech, ub_cus])
        dim = lb.shape[1]
        return [lb, ub, dim, fobj]
    
    # selection function
    if F == "Swap_TypeA":
        fobj = Swap_TypeA
        lb = np.zeros([1, 3])
        ub_swap = np.ones([1, 2]) * num_cust
        ub_gen_route = np.array([[3]])
        ub = np.hstack([ub_gen_route, ub_swap])
        dim = lb.shape[1]
        return [lb, ub, dim, fobj]
    
    # selection function
    if F == "Swap_TypeB":
        fobj = Swap_TypeB
        lb = np.zeros([1, 3])
        ub_swap = np.ones([1, 2]) * num_cust
        ub_gen_route = np.array([[3]])
        ub = np.hstack([ub_gen_route, ub_swap])
        dim = lb.shape[1]
        return [lb, ub, dim, fobj]