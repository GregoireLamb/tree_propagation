import math
import numpy as np
from random import random
#from src.utils import compute_height_level


class Tree:
    # rewrite with lower case
    def __init__(self, id, lat, long, species, height, age, spreading_factor):
        self.id = id
        self._lat = lat
        self._long = long
        self._species = species
        self._height_level = height
        self._age = age
        self._spreading_factor = spreading_factor
        self._alive = True

    def __repr__(self):
        return f"Tree(id:{self.id}, position:({self._lat}{self._long}), group:{self._species}, height:{self._height_level}, age:{self._age})"

    def update(self, config):
        # TODO adapt individual rules here

        from src.utils import compute_height_level, eval_mortality, wind_blow, seed_spread

        # update the age of the tree
        self._age += 1

        # Update the height level of the tree with the Chapman-Richards growth model
        self._height_level = compute_height_level(self._age)
        # DEPR  self._height_level += self._height_level * 5 / 100

        # Decide if tree dies
        self._alive = eval_mortality(self._age)
        #TODO if surroundings are too crowded

        # Blow seeds to target
        # TODO seed generation
        target_lat, target_long = wind_blow(self._lat, self._long, (np.random.uniform(-1, 1), np.random.uniform(-1, 1)), np.random.randint(0, 35), self._spreading_factor)
        #seeding_radius = config.default_seeding_radius
        #seed_spread((target_lat, target_long), self._height_level, seeding_radius)

        # print(self._age)
        return target_lat, target_long #TODO retun as a list

        # DEPR
        #rnd = 30 * random() # random number between 0 and 10
        #if math.exp(self._age / 100) > rnd:
        #    self._alive = False
        #    return -1
