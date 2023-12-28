import pandas as pd
from src.tree import Tree

def import_data(config):
    df = pd.read_csv(config.data_path + config.data_file, sep=',', index_col=0)
    return df

def observe_data(df):
    print(df.describe())
    print(df.info())

def make_trees(df):
    forest = []
    for tree in df.iterrows():
        forest.append(Tree(tree[0],
                           tuple(map(float, tree[1]["SHAPE"].split('(')[1].split(')')[0].split())),
                           tree[1]["GRUPPE"],
                           tree[1]["BAUMHOEHE"],
                           tree[1]["ALTERab2023"]))
    return forest

def run_simulation(population, config, visualize):
    # TODO add a progress bar
    for year in range(config.simulation_duration):
        print(f"{year/config.simulation_duration*100:.2f}% done")
        visualize.create_visualisation_step(population, year)
        population.update()

    visualize.create_visualisation_step(population, config.simulation_duration)
