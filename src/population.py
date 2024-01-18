import pandas as pd
from src.tree import Tree
from src.utils import *

class Population:
    def __init__(self):
        self._trees = []
        self._trees_alive = []

        self._tree_groups = None
        self._statistic = None
        self._starting_year = 2023

    def __repr__(self):
        return (f"Population: "+
                f"\n\t- Started in year {self._starting_year}"+
                f"\n\t- {len(self._trees)} trees in total"+
                f"\n\t- {len(self._trees) - len(self._trees_alive)} trees dead"+
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
        self._trees = make_trees(df)
        self._trees_alive = self._trees.copy()
        self._tree_groups = list(set([tree._grouppe for tree in self._trees]))

        trees_per_group = {}
        for group in self._tree_groups:
            trees_per_group[group] = 0
        for tree in self._trees:
            trees_per_group[tree._grouppe] += 1

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

    def get_trees(self, id):
        return self._trees[id]

    def update_trees_statistics(self):
        # count the amount of trees per group self._tree_groups
        trees_per_group = {}
        for group in self._tree_groups:
            trees_per_group[group] = 0
        for tree in self._trees_alive:
            trees_per_group[tree._grouppe] += 1

        new_row = {'year': self._statistic.iloc[-1]['year'] + 1, 'population_size': len(self._trees_alive)}
        new_row.update(trees_per_group)

        self._statistic.loc[len(self._statistic)] = new_row
        return trees_per_group


    def update(self):
        for tree in self._trees_alive:
            if tree.update() == -1:
                self.remove_tree(tree)

        # TODO adapt group rules here

        self.update_trees_statistics()