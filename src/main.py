import random

# import matplotlib.pyplot as plt

from src.config import Config
from src.utils import import_data, observe_data, run_simulation
from src.visualisation import *
from src.population import *
from src.visualisation import *


def main():
    print("\t-- Loading config...\n")
    config = Config()
    random.seed(config.seed)

    # Data basic stat
    data = import_data(config)
    #observe_data(data)

    # Create population
    population = Population()
    population.populate(data)
    visualize = Visualisation()
    visualize.set_group_color_mapping(population._tree_groups)
    print(population)

    print("\n\t-- Simulation ready.")

    run_simulation(population, config, visualize)

    visualize.make_gif()
    population.plot_statistic()


if __name__ == '__main__':
    main()
