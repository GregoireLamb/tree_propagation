import math
import numpy as np
import random
# from src.utils import compute_height_level
from geographiclib.geodesic import Geodesic
from shapely.geometry import Point


class Tree:
    # rewrite with lower case
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

    def update(self, config):
        # Adapt individual rules here
        self._age += 1
        self._height_level = self.compute_height_level(self._age)
        self._alive = self.eval_mortality(self._age)

        if self._alive:
            # Blow seeds to target
            tree_seeds = self.seeding(self._lat, self._long, (np.random.uniform(-1, 1), np.random.uniform(-1, 1)),
                                      np.random.randint(0, 35), self._spreading_factor, config)
            # TODO assert seed are valid and pre filter
            return tree_seeds
        return []


    def seeding(self, start_lat, start_long, wind_direction, wind_strength, spreading_factor, config):

        # Calculate bearing of the wind in degrees (0 is North)
        bearing = np.degrees(np.arctan2(*wind_direction[::-1])) % 360.0

        # Determine distance vector from input factors
        distance_meters = wind_strength * spreading_factor

        # Set to World Geodetic System 1984 (GPS standard)
        geod = Geodesic.WGS84
        # Calculate center of new seeds
        seeding_center = geod.Direct(start_lat, start_long, bearing, distance_meters)

        # vienna_bounding_box = [48.12, 16.18, 48.32, 16.58]
        #
        # # Check if the position is inside the map boundaries (assuming a square map of vienna)
        # if seeding_center['lat2'] > vienna_bounding_box[0] or seeding_center['lat2'] < vienna_bounding_box[2] or \
        #         seeding_center['lon2'] > vienna_bounding_box[1] or seeding_center['lon2'] < vienna_bounding_box[3]:
        return self.generate_random_seeds(lat_center=seeding_center['lat2'], long_center=seeding_center['lon2'], config=config)

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
        slope = 0.8  # Slope of growth

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

    # TODO: Offset of center point along the major axis (depending on wind strength)?
    # TODO: adjust axis lengths
    # TODO: make seed_amount a Tree() attribute? is not fixed, height changes...
    def generate_random_seeds(self, lat_center, long_center, config):
        """
        Generate random seeds within the area of an ellipse that is defined by the center point

        Parameters:
        -

        Returns:
        - List of tuples with generated points as tuples (latitude, longitude) and species information.
        """
        germinating_seed_amount = config.seed_amount_map[self._height_level]
        # germination_rate = 0.001  # TODO as constant in config?
        # germinating_seed_amount = seed_amount * germination_rate

        major_axis, minor_axis = 0.01, 0.005  # in kilometers # TODO make dependent on wind_strength & spreading_factor and change to meters

        center_point = Point(long_center, lat_center)  # Shapely Point uses (longitude, latitude)

        ellipse_bbox = center_point.buffer(1).envelope
        seed_points = []

        while len(seed_points) < germinating_seed_amount:
            random_point = Point(
                random.uniform(ellipse_bbox.bounds[0], ellipse_bbox.bounds[2]),
                random.uniform(ellipse_bbox.bounds[1], ellipse_bbox.bounds[3])
            )

            if ellipse_bbox.contains(random_point):
                seed_points.append((random_point.y, random_point.x))

        return [(seed_point, self._species) for seed_point in seed_points]


        # # Visualize bbox + random points
        # plt.scatter(*zip(*random_ellipse_points))
        # plt.plot(*ellipse_bbox.exterior.xy)
        # plt.xlabel('Longitude')
        # plt.ylabel('Latitude')
        # plt.title('Random Points Within Ellipse')
        # plt.grid(True)
        # plt.show()