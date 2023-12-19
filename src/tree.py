import math
from random import random


class Tree:
    # rewrite with lower case
    def __init__(self, id, shape, grouppe, baumoehe, alterAb2023):
        self.id = id
        self._gps = shape
        self._grouppe = grouppe
        self._baumoehe = baumoehe
        self._alterAb2023 = alterAb2023
        self._spreading_factor = None
        self._alive = True

    def __repr__(self):
        return f"Tree({self.id}, position:{self._gps}, group:{self._grouppe}, height:{self._baumoehe}, age:{self._alterAb2023})"

    def update(self):
        # TODO adapt individual rules here
        # update the age of the tree
        self._alterAb2023 += 1

        # update the height of the tree
        self._baumoehe += self._baumoehe*5/100

        rnd = 30 * random() # random number between 0 and 10
        if math.exp(self._alterAb2023/100) > rnd:
            self._alive = False
            return -1
