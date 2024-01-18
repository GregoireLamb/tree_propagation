import pandas as pd
from src.tree import Tree
from src.utils import *
import matplotlib.pyplot as plt

from src.tree import Tree


class Population:
    def __init__(self):
        self._trees = []
        self._trees_alive = []

        self._tree_groups = None
        self._statistic = None
        self._starting_year = 2024
        self._current_tree_id = 168880  # extract max id from initial df
        # self._simulation_counter = 0    # keep track of simulation years to increment tree level

    def __repr__(self):
        return (f"Population: " +
                f"\n\t- Started in year {self._starting_year}" +
                f"\n\t- {len(self._trees)} trees in total" +
                f"\n\t- {len(self._trees) - len(self._trees_alive)} trees dead" +
                f"\n\n\t- Population statistic\n{self._statistic}")

    def plot_statistic(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(self._statistic['year'], self._statistic['population_size'])
        for group in self._tree_groups:
            ax.plot(self._statistic['year'], self._statistic[group])

        ax.legend(['population_size'] + self._tree_groups, bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xlabel('Year')
        ax.set_ylabel('Population size')
        ax.set_title('Population size over time')

        plt.tight_layout()  # Ensures the legend fits within the figure
        plt.show()

    def populate(self, df):
        self._trees = create_trees(df)
        self._trees_alive = self._trees.copy()

        print("Length Trees Alive:", len(self._trees_alive))

        self._tree_groups = list(set([tree._species for tree in self._trees]))

        trees_per_group = {}
        for group in self._tree_groups:
            trees_per_group[group] = 0
        for tree in self._trees:
            trees_per_group[tree._species] += 1

        stat_columns = ['year', 'population_size'] + self._tree_groups
        self._statistic = pd.DataFrame(columns=stat_columns)
        # init the statistic with the starting year
        initial_row = {'year': self._starting_year, 'population_size': len(self._trees)}
        initial_row.update(trees_per_group)

        self._statistic.loc[0] = initial_row
        print(self._statistic)

    def add_tree(self, tree):
        self._trees.append(tree)
        self._trees_alive.append(tree)

    def remove_tree(self, tree):
        self._trees_alive.remove(tree)
        #self._trees.remove(tree)

    def get_trees(self, id):
        return self._trees[id]

    def update_trees_statistics(self):
        # count the amount of trees per group self._tree_groups
        trees_per_group = {}
        for group in self._tree_groups:
            trees_per_group[group] = 0
        for tree in self._trees_alive:
            trees_per_group[tree._species] += 1

        new_row = {'year': self._statistic.iloc[-1]['year'] + 1, 'population_size': len(self._trees_alive)}
        new_row.update(trees_per_group)

        self._statistic.loc[len(self._statistic)] = new_row
        return trees_per_group

    def update_forest(self, config):

        forest_seeds = []

        for tree in self._trees_alive:
            # Get list of seed originating from tree
            tree_seeds = tree.update(config)
            # Append to forest seed list
            forest_seeds.append(tree_seeds)

            # Possibly remove old tree from forest
            if not tree._alive:
                self.remove_tree(tree)

        forest_seeds_flat = [seed for tree_seeds in forest_seeds for seed in tree_seeds]

        # TODO adapt group rules here
        for seed in forest_seeds_flat:
            # TODO decide if seed becomes tree
            # Create new tree on new position
            self._current_tree_id += 1

            new_tree = Tree(self._current_tree_id,
                            target_lat,
                            target_long,
                            tree._species,
                            0,
                            0,
                            tree._spreading_factor)

            # Add new tree to forest
            self.add_tree(new_tree)

        self.update_trees_statistics()
