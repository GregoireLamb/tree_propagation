import sys
from operator import attrgetter

import pandas as pd
from src.tree import Tree
import matplotlib.pyplot as plt
import random
import bisect
from alive_progress import alive_bar

from src.tree import Tree
from src.utils import *


class Population:
    def __init__(self):
        self._trees = []
        self._trees_alive = []
        self.species_label_map = None

        self._tree_groups = None
        self._statistic = None
        self._starting_year = 2024
        self._current_tree_id = 168880  # extract max id from initial df

    def __repr__(self):
        stat_to_print = self._statistic.rename(columns=self.species_label_map)
        return (f"Population: " +
                f"\n\t- Started in year {self._starting_year}" +
                f"\n\t- {len(self._trees)} trees in total" +
                f"\n\t- {len(self._trees) - len(self._trees_alive)} trees dead" +
                f"\n\n\t- Population statistic\n{stat_to_print}")

    def plot_statistic(self, config):
        # Print and save plots
        self.plot_population_group_over_time(config.species_label_map, config.result_path,
                                             show_plot_on_the_fly=config.show_plot_on_the_fly)
        self.plot_cumul_group_over_time(config.species_label_map, config.result_path,
                                        show_plot_on_the_fly=config.show_plot_on_the_fly)
        self.plot_proportional_group_over_time(config.species_label_map, config.result_path,
                                               show_plot_on_the_fly=config.show_plot_on_the_fly)

        # Save the logs in csv
        with open(config.result_path + 'log.txt', 'w') as file:
            sys.stdout = file  # Redirect standard output to the file
            print(self)
            sys.stdout = sys.__stdout__

        # save stat as csv
        stat_to_print = self._statistic.rename(columns=self.species_label_map)
        stat_to_print.to_csv(config.result_path + 'Population_evolution.csv', index=False)

    def plot_proportional_group_over_time(self, species_label_map, save_path, show_plot_on_the_fly):
        fig, ax = plt.subplots(figsize=(10, 6))
        stat = self._statistic.copy()
        year = stat["year"].values
        stat = stat[self._tree_groups]
        stat = stat.rename(columns=species_label_map)

        # Calculate proportions
        stat_proportions = stat.div(stat.sum(axis=1), axis=0)

        ax.stackplot(year, stat_proportions.values.T,
                     labels=stat_proportions.columns, alpha=0.8)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xlabel('Year')
        ax.set_ylabel('Proportion')
        ax.set_title('Proportion of each species over time')

        plt.tight_layout()  # Ensures the legend fits within the figure
        plt.savefig(save_path + "Group_proportion_evolution.png")
        if show_plot_on_the_fly:
            plt.show()
        plt.clf()

    def plot_cumul_group_over_time(self, species_label_map, save_path, show_plot_on_the_fly):
        fig, ax = plt.subplots(figsize=(10, 6))
        stat = self._statistic.copy()
        year = stat["year"].values
        stat = stat[self._tree_groups]
        stat = stat.rename(columns=species_label_map)
        stat = stat.to_dict(orient='list')
        # map stat key to group_name_mapping key

        ax.stackplot(year, stat.values(),
                     labels=stat.keys(), alpha=0.8)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xlabel('Year')
        ax.set_ylabel('Population size')
        ax.set_title('Population size over time (cumul)')

        plt.tight_layout()  # Ensures the legend fits within the figure
        plt.savefig(save_path + "population_cumul_evolution.png")
        if show_plot_on_the_fly:
            plt.show()
        plt.clf()

    def plot_population_group_over_time(self, species_label_map, save_path, show_plot_on_the_fly):
        fig, ax = plt.subplots(figsize=(10, 6))
        for group in self._tree_groups:
            ax.plot(self._statistic['year'], self._statistic[group], label=species_label_map[group])

        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xlabel('Year')
        ax.set_ylabel('Population size')
        ax.set_title('Population size over time')

        plt.tight_layout()  # Ensures the legend fits within the figure
        plt.savefig(save_path + "population_evolution.png")
        if show_plot_on_the_fly:
            plt.show()
        plt.clf()

    def populate(self, df, config):
        self.species_label_map = config.species_label_map
        initial_forest = self.create_trees(df)

        # Assert initial trees are in the simulation environment
        for tree in initial_forest:
            if (config.bounding_box[0][0] <= tree._lat <= config.bounding_box[1][0] and
                    config.bounding_box[0][1] <= tree._long <= config.bounding_box[1][1]):
                self._trees.append(tree)

        self._trees_alive = self._trees.copy()
        self._trees_alive = sorted(self._trees_alive, key=attrgetter('_lat', '_long'))
        print("Number of Trees Alive:", len(self._trees_alive))

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

    def add_tree(self, tree, alive_indice):
        self._trees.append(tree)
        self._trees_alive.append(tree)
        self._trees_alive = sorted(self._trees_alive, key=lambda t: (t._lat, t._long))

    def remove_trees(self, trees):
        for tree in trees:
            self._trees_alive.remove(tree)

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

    def update_forest(self, config, year):
        year = year + self._starting_year

        forest_seeds = []
        i = 0
        trees_to_remove = []

        # TODO add to logs
        # TODO get strategy from config
        wind_direction = np.random.uniform(0, 360)
        wind_strength = np.random.randint(0, 35)

        with alive_bar(total=len(self._trees_alive), title=f"Update Trees: [{year}]".format(i),
                       spinner='classic') as bar:  # len(train_loader) = n_batches
            for i, tree in enumerate(self._trees_alive):
                # Update each tree
                tree_seeds = tree.update(config, wind_direction, wind_strength)
                forest_seeds = forest_seeds + tree_seeds

                if not tree._alive:
                    trees_to_remove.append(tree)
                bar()

            # remove trees
            self.remove_trees(trees_to_remove)

        # Adapt group rules here
        n_seed = len(forest_seeds)
        planted = 0
        with alive_bar(total=n_seed, title="Plant seed Trees: ".format(planted),
                       spinner='classic') as bar:  # len(train_loader) = n_batches
            while forest_seeds:
                # Decide if seed becomes tree -> if enough space around
                random_index = random.randint(0, len(forest_seeds) - 1)
                seed = forest_seeds.pop(random_index)
                planted += 1
                indice = self.seed_has_enough_space_around(seed,
                                                           radius=config.seed_living_space)  # retun -1 if not enough space, indice for insertion otherwise
                if indice != -1:  # TODO here adapt radius
                    # Create new tree on new position
                    self._current_tree_id += 1
                    # print(f'new seed: {seed}')

                    new_tree = Tree(self._current_tree_id,
                                    seed[0][0],
                                    seed[0][1],
                                    seed[1],
                                    0,
                                    0,
                                    get_spreading_factor_from_species(seed[1]))

                    # Add new tree to forest
                    self.add_tree(new_tree, indice)  # TODO insert at right place
                bar()
            self.update_trees_statistics()

    def seed_has_enough_space_around(self, seed, radius):
        trees, start_index, stop_index = self.trees_in_the_surroundings(seed[0][0], seed[0][1], radius)
        # if len(trees) != 0: print(len(trees))
        for tree in trees:
            if distance_between_coordinate(tree._lat, tree._long, seed[0][0], seed[0][1]) < radius:
                return -1
        switch = bisect.bisect_left(KeyWrapper(trees, key=lambda t: (t._lat, t._long)),
                                    (seed[0][0], seed[0][1]))
        return start_index + switch

    def trees_in_the_surroundings(self, lat, long, radius):
        # binary search
        lat_min, long_min, lat_max, long_max = box_around_lat_long(lat, long, radius)
        start_index = bisect.bisect_left(KeyWrapper(self._trees_alive, key=lambda t: (t._lat, t._long)),
                                         (lat_min, long_min))
        start_index = max(0, min(start_index, len(self._trees_alive) - 1))
        # reverse = self._trees_alive[::-1]
        end_index = bisect.bisect_left(KeyWrapper(self._trees_alive[::-1], key=lambda t: (t._lat, t._long)),
                                        (lat_max, long_max))
        end_index = len(self._trees_alive)-end_index
        end_index = max(0, min(end_index, len(self._trees_alive) - 1))

        #TODO remove
        start_index = 0
        end_index = len(self._trees_alive)-1

        return self._trees_alive[start_index:end_index], start_index, end_index

    def create_trees(self, df):
        forest = []
        for row in df.iterrows():
            location = row[1]["SHAPE"].split("(")[1].split(")")[0].split()
            forest.append(Tree(row[0],
                               float(location[1]),
                               float(location[0]),
                               row[1]["GRUPPE"],
                               row[1]["BAUMHOEHE"],
                               row[1]["ALTERab2023"],
                               get_spreading_factor_from_species(row[1]["GRUPPE"])))
        return forest


class KeyWrapper:
    def __init__(self, iterable, key):
        self.it = iterable
        self.key = key

    def __getitem__(self, i):
        return self.key(self.it[i])

    def __len__(self):
        return len(self.it)

    def insert(self, index, item):
        print('asked to insert %s at index%d' % (item, index))
        self.it.insert(index, item)
