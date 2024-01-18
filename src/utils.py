import pandas as pd
import numpy as np
import math
import json
from geographiclib.geodesic import Geodesic

from src.tree import Tree

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
    #print(config.data_path + config.data_file)
    #print(config.data_path + config.species_mapping_file)
    df = pd.read_csv(config.data_path + config.data_file, sep=',', index_col=0)

    with open(config.data_path + config.species_mapping_file, 'r', encoding='utf-8') as f:
        species_mapping = json.load(f)
    df = df.replace({"GRUPPE": species_mapping})
    return df


def observe_data(df):
    print(df.head(15))
    print(df.describe())
    print(df.info())


def create_trees(df):
    forest = []
    for row in df.iterrows():
        location = row[1]["SHAPE"].split("(")[1].split(")")[0].split()
        forest.append(Tree(row[0],
                           float(location[1]),
                           float(location[0]),
                           row[1]["GRUPPE"],
                           row[1]["BAUMHOEHE"],
                           row[1]["ALTERab2023"],
                           spreading_factor_map[row[1]["GRUPPE"]]))
    return forest


def run_simulation(population, config, visualize):
    # TODO add a progress bar
    for year in range(config.simulation_duration):
        print(f"{year / config.simulation_duration * 100:.2f}% done")
        visualize.create_visualisation_step(population, year)
        population.update_forest(config)
    visualize.create_visualisation_step(population, config.simulation_duration)


def compute_height_level(age):
    """
    Computes the Chapman-Richards growth model

    Returns the height level of a tree

    Parameters
    ----------
    age : age
    alpha : upper asymptote
    beta : growth range
    rate : growth rate
    slope : slope of growth

    References
    ----------
    .. [1] D. Fekedulegn, M. Mac Siurtain, and J. Colbert, "Parameter estimation
           of nonlinear growth models in forestry," Silva Fennica, vol. 33,
           no. 4, pp. 327-336, 1999.
    """

    alpha = 50  # Upper asymptote (max tree height)
    beta = 0.8  # Growth range
    rate = 0.08  # Growth rate
    slope = 0.8  # Slope of growth

    # flooring results to the next int
    result = math.floor(alpha * (1 - beta * np.exp(-rate * age)) ** (1 / (1 - slope)))

    if result == 0:
        return 0
    else:
        level = (result - 1) // 5 + 1
        return min(level, 8)


def eval_mortality(age):
    """
    Determines if a tree is alive or dead based on a organism mortality probability distribution.

    Returns a boolean with True if tree gets to live on

    Parameters
    ----------
    age : age
    alpha : upper asymptote
    beta : growth range
    rate : growth rate
    slope : slope of growth

    References
    ----------
    Petrovska, R., Bugmann, H., Hobi, M., Ghosh, S., & Brang, P. (2022).
    Survival time and mortality rate of regeneration in the deep shade of a primeval beech forest.
    European Journal of Forest Research, 141. https://doi.org/10.1007/s10342-021-01427-3
    """
    alpha = 1  # Upper asymptote
    beta = 0.7  # Growth range
    rate = 0.05  # Growth rate
    slope = 0.9  # Slope of growth
    delta = 0.8  # Clip bottom values

    survival_probability = 1 - (alpha * (1 - beta * np.exp(-rate * age)) ** (1 / (1 - slope)) * delta)

    random_number = np.random.random()  # Generate a random number between 0 and 1

    return random_number < survival_probability


def scale_to_lat_long(unit_vector, lat):
    """
    DEPRECATED
    """
    # Using estimate that 111,111 meters (111.111 km) in the y direction is 1 degree (of latitude)
    # and 111,111 * cos(latitude) meters in the x direction is 1 degree (of longitude).
    # Latitude
    lat_offset = (1 + unit_vector[0]) / 111111

    # Longitude (East is positive, West is negative)
    long_offset = (1 + unit_vector[1]) / (111111 * np.cos(lat))

    return np.array([lat_offset, long_offset])


def wind_blow(start_lat, start_long, wind_direction, wind_strength, spreading_factor):
    # Convert wind direction into a unit vector ## DEPR: using degrees now
    # wind_direction = np.array([wind_direction[0], wind_direction[1]])
    # wind_direction = wind_direction / np.linalg.norm(wind_direction)

    # Calculate bearing of the wind in degrees (0 is North)
    bearing = np.degrees(np.arctan2(*wind_direction[::-1])) % 360.0

    # Determine distance vector from input factors
    distance_meters = wind_strength * spreading_factor

    # Set to World Geodetic System 1984 (GPS standard)
    geod = Geodesic.WGS84
    destination_point = geod.Direct(start_lat, start_long, bearing, distance_meters)

    vienna_bounding_box = [48.12, 16.18, 48.32, 16.58]

    # Check if the position is outside the map boundaries (assuming a square map of vienna)
    if destination_point['lat2'] < vienna_bounding_box[0] or destination_point['lat2'] > vienna_bounding_box[2] or \
            destination_point['lon2'] < vienna_bounding_box[1] or destination_point['lon2'] > vienna_bounding_box[3]:
        # print("OUT OF BOUNDS")
        return False, False

    return destination_point['lat2'], destination_point['lon2']


def seed_spread(center_pos, tree_height_level, min_seeding_radius):
    planted_seeds = []

    return planted_seeds
