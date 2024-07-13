import numpy as np
from utils import Test_Function

def euclidean_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


class Delivery_Route(Test_Function):
    def __init__(
            self,
            route_map,
            price,
            dim=5, 
            lb=np.ones_like([np.arange(5)])*0, 
            ub=np.ones_like([np.arange(5)])*5):
        super().__init__(dim, lb, ub)
        self.route_map = route_map
        self.price = price
    
    def get_score(self, route):
        total_distance = 0
        route = [round(i) for i in route]
        
        if len(route) != len(set(np.unique(route))):
            random_path = np.random.permutation(np.arange(len(route))[1:])
            return self.get_score(random_path)

        for idx in range(1, len(route)):
            point1 = self.route_map[self.route_map['code']==route[idx-1]][['latitude', 'longitude']].values
            point2 = self.route_map[self.route_map['code']==route[idx-2]][['latitude', 'longitude']].values
            total_distance += euclidean_distance(point1[0], point2[0])
            total_cost = total_distance * self.price

        # TODO: include deport into calculation

        # change to maximization
        fitness = 1/total_cost

        if fitness == 0:
            print(route)

        return fitness, route
    

    def get_total_cost(self, route):
        total_distance = 0

        for idx in range(1, len(route)):
            point1 = self.route_map[self.route_map['code']==route[idx-1]][['latitude', 'longitude']].values
            point2 = self.route_map[self.route_map['code']==route[idx-2]][['latitude', 'longitude']].values
            total_distance += euclidean_distance(point1[0], point2[0])
            total_cost = total_distance * self.price

        return total_cost
            


    