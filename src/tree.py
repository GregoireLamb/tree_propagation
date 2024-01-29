import random

import numpy as np
from geographiclib.geodesic import Geodesic

from src.utils import *


class Tree:
    """
    Class representing each tree
    """

    def __init__(self, id, lat, long, species=1, height=0, age=0, spreading_factor=1):
        self.id = id
        self._lat = lat
        self._long = long
        self._species = species
        self._height_level = height
        self._age = age
        self._spreading_factor = spreading_factor
        self._alive = True

    def __repr__(self):
        return f"Tree(id:{self.id}, position:({self._lat}, {self._long}), group:{self._species}, height:{self._height_level}, age:{self._age})"

    def update(self, config, wind_direction, wind_strength):
        """
        Main update function for the trees:
            -   Adapt age, height
            -   Decide if the tree is alive
            -   Generate seeds
        :return: list of seeds
        """
        # Adapt individual rules here
        self._age += 1
        self._height_level = self.compute_height_level(self._age)
        self._alive = self.eval_mortality(self._age)

        if self._alive:
            tree_seeds = self.seeding(self._lat, self._long, wind_direction, wind_strength, self._spreading_factor,
                                      config)
            return tree_seeds
        return []

    def seeding(self, start_lat, start_long, wind_direction, wind_strength, spreading_factor, config):
        """"
        Generate tree seeds
        Method: generate seeds from random position in a circle whose center is at wind_strength * spreading_factor from the acctual tree
        the circle radius is default factor * spreading factor
        """
        # Calculate bearing of the wind in degrees (0 is North)
        bearing = wind_direction

        # Determine distance vector from input factors
        distance_meters = wind_strength * spreading_factor

        # Calculate center of circle new seeds
        seeding_center = Geodesic.WGS84.Direct(start_lat, start_long, bearing, distance_meters)

        return self.generate_random_seeds(lat_center=seeding_center['lat2'], long_center=seeding_center['lon2'],
                                          config=config, radius=config.default_seeding_radius * spreading_factor)

    def compute_height_level(self, age):
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
        slope = 0.3  # Slope of growth

        # flooring results to the next int
        result = math.floor(alpha * (1 - beta * np.exp(-rate * age)) ** (1 / (1 - slope)))

        if result == 0:
            return 0
        else:
            level = (result - 1) // 5 + 1
            return min(level, 8)

    def eval_mortality(self, age):
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

    def generate_random_seeds(self, lat_center, long_center, config, radius):
        """
        Generate random point within the seeding circle
        Use polar coordinate for time efficiency
        """
        germinating_seed_amount = int(config.seed_amount_map[self._height_level] * 0.1) # Keep propotions

        seed_points = []
        EarthRadius = 6371000.0

        for seed in range(germinating_seed_amount):
            # Generate random angle
            theta = random.uniform(0, 2 * math.pi)
            # Generate a random radius within the specified circle
            r = random.uniform(0, radius)

            # Convert polar coordinates to Cartesian coordinates
            x = r * math.cos(theta)
            y = r * math.sin(theta)

            # Convert Cartesian coordinates to latitude and longitude
            lat_final = math.degrees(math.asin(math.sin(math.radians(lat_center)) * math.cos(y / EarthRadius) +
                                               math.cos(math.radians(lat_center)) * math.sin(y / EarthRadius)))

            lon_final = math.degrees(math.radians(long_center) + x / EarthRadius) % 360

            # Check if the generated point is within the bounding box
            if (config.bounding_box[0][0] <= lat_final <= config.bounding_box[1][0] and
                    config.bounding_box[0][1] <= lon_final <= config.bounding_box[1][1]):
                seed_points.append(((lat_final, lon_final), self._species))

        return seed_points
