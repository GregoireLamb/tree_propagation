import json
import math
from math import radians, sin, cos, sqrt, atan2

import pandas as pd

"""
This file contains utility functions for the simulation such a loading function or computation function 
"""

# seed_amount = None

spreading_factor_map = {
    1: 1.5,
    2: 1.2,
    3: 0.4,
    4: 1.1,
    5: 0.2,
    6: 1.0,
    7: 0.9,
    8: 1.3,
    9: 1.8,
    10: 0.7,
    11: 0.8
}


def import_data(config):
    """
    Load the initial data in a dataframe
    """
    df = pd.read_csv(config.data_path + config.data_file, sep=',', index_col=0)

    with open(config.data_path + config.species_mapping_file, 'r', encoding='utf-8') as f:
        species_mapping = json.load(f)
    df = df.replace({"GRUPPE": species_mapping})
    return df


def run_simulation(population, config, visualize):
    """
    Main loop of the simulation
    Runs the population updates and visualisation creation for every generation
    """
    for year in range(config.simulation_duration):
        visualize.create_visualisation_step(population, year, config.result_path)
        population.update_forest(config, year)
    visualize.create_visualisation_step(population, config.simulation_duration, config.result_path)


def distance_between_coordinate(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two coordiantes using haversine distance
    :return: distance in meter
    """
    earth_radius = 6371000.0
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius * c


def get_spreading_factor_from_species(species: int):
    """
    Getter function
    """
    return spreading_factor_map[species]


def box_around_lat_long(original_latitude, original_longitude, meters_difference):
    """
    Return latitudes and logiture around a given coordinate using a simplifying estimation of
    the convertion from degrees to meters
    """
    # Simplified version where 1m = 1/111.11 in lat and 1m = 111.11*cos(lat) in long
    diff_lon = 1 / (meters_difference * 111.11 * math.cos(math.radians(original_latitude)))
    diff_lat = meters_difference / 111.11
    latitude_down = original_latitude - diff_lat
    latitude_up = original_latitude + diff_lat
    longitude_left = original_longitude - diff_lon
    longitude_right = original_longitude + diff_lon
    return latitude_down, longitude_left, latitude_up, longitude_right


def observe_data(df):
    print(df.head(15))
    print(df.describe())
    print(df.info())
