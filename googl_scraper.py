# %% Imports
import os
import time
import json
import random
import pandas as pd
from itertools import combinations
from utils import SeleniumGoogleMap

# %% Helper function
def get_coors(stores_code: tuple, df: pd.DataFrame):
    assert len(stores_code)==2, "Input should be between 2 stores"

    if "code" not in df or "latitude" not in df or "longitude" not in df:
        "Please recheck the input dataframe"

    origin = stores_code[0]
    destination = stores_code[1]

    origin = df[df['code']==origin][['latitude', 'longitude']].values
    destination = df[df['code']==destination][['latitude', 'longitude']].values

    origin = f"{origin[0][0]}, {origin[0][1]}"
    destination = f"{destination[0][0]}, {destination[0][1]}"
    return origin, destination


def get_distances(version, stores_combination, df):
    # Load scraper
    scraper = SeleniumGoogleMap()
    scraper.open_map()
    scraper.initial_location()
    scraper.initiate_direction()
    scraper.get_direction()

    routes = {
        "version": version,
        "routes": []
    }

    if type(stores_combination) == list:
        for idx, coor in enumerate(stores_combination):
            # get coordinate
            origin, destination = get_coors(coor, df)

            # time delay
            time.sleep(random.randint(1, 10))

            # get direction & distance
            scraper.get_direction(origin, destination)
            distances = scraper.get_distance()

            # collector
            route = {
                'route_id': idx,
                'start_location_code': coor[0],
                'end_location_code': coor[1],
                'distances': []
            }

            for distance in distances:
                route['distances'].append(distance)

            routes['routes'].append(route)

    else:
        origin, destination = get_coors(stores_combination, df)
        scraper.get_direction(origin, destination)
        distances = scraper.get_distance()

        # collector
        route = {
            'route_id': 1,
            'start_location_code': stores_combination[0],
            'end_location_code': stores_combination[1],
            'distances': []
        }

        for distance in distances:
            route['distances'].append(distance)

        routes['routes'].append(route)

    return routes

# %% Pathing
MAIN_PATH = os.getcwd()
SBH_LOCATIONS = os.path.join(MAIN_PATH, "01-99speedmart", "data", "sbh_locations.csv")
SBH_DISTANCE = os.path.join(MAIN_PATH, "01-99speedmart", "data", "sbh_distance.json")

if __name__ == "__main__":
    # TODO: need to implement multiple states
    # Load sabah stores
    df_stores = pd.read_csv(SBH_LOCATIONS)

    # Get combinations
    stores_combination = [combo for combo in combinations(df_stores['code'], 2)]

    # Scrape distance
    distances = get_distances(1, stores_combination, df_stores)

    # Saving as json
    with open(SBH_DISTANCE, 'w') as f:
        json.dump(distances, f)
