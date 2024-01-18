import pandas as pd
import numpy as np
import math
import json

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


def get_seed_amount(config, height_level):
    with open(config.data_path + config.seed_amount_file, 'r', encoding='utf-8') as f:
        seed_amount_map = json.load(f)

    seed_amount = seed_amount_map[height_level]

    return seed_amount
