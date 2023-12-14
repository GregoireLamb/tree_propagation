import pandas as pd
from src.tree import Tree
from src.utils import *

class Population:
    def __init__(self):
        self._trees = []
        self._trees_alive = []
        self._population_size_evolution = []
        self._year = 2023
        self._starting_year = 2023
        self._tree_groups = []

    def __repr__(self):
        pop_stat = self.get_trees_statistics()
        return (f"Population: "+
                f"\n\t- Started in year {self._year}"+
                f"\n\t- Current year {self._year}"+
                f"\n\t- {len(self._trees)} trees in total"+
                f"\n\t- {len(self._trees_alive)} trees alive"+
                f"\n\t- {len(self._trees) - len(self._trees_alive)} trees dead"+
                f"\n\n\t- Population statistic\n{pop_stat}")

    def populate(self, df):
        self._trees = make_trees(df)
        self._trees_alive = self._trees.copy()
        self._tree_groups = list(set([tree._grouppe for tree in self._trees]))

    def add_tree(self, tree):
        self._trees.append(tree)
        self._trees_alive.append(tree)

    def remove_tree(self, tree):
        self._trees_alive.remove(tree)

    def get_trees(self, id):
        return self._trees[id]

    def get_trees_statistics(self):
        # count the amount of trees per group self._tree_groups
        trees_per_group = {}
        for group in self._tree_groups:
            trees_per_group[group] = 0
        for tree in self._trees:
            trees_per_group[tree._grouppe] += 1
        # make trees_per_group a dataframe
        trees_per_group = pd.DataFrame.from_dict(trees_per_group, orient='index', columns=['amount'])
        # add the percentage of trees per group
        trees_per_group['proportion'] = trees_per_group['amount'] / len(self._trees) * 100
        return trees_per_group


    def update(self):
        pass