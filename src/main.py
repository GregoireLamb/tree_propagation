import random

# import matplotlib.pyplot as plt

from src.config import Config
from src.population import *
from src.visualisation import *


def main():
    print("\t-- Loading config...\n")
    config = Config()
    random.seed(config.seed)

    # Data basic stat
    data = import_data(config)

    # Create population
    population = Population()
    population.populate(data)
    visualize = Visualisation(config)
    visualize.set_group_color_mapping(population._tree_groups)
    print(population)

    print("\n\t-- Simulation ready.")

    run_simulation(population, config, visualize)

    visualize.make_gif()
    population.plot_statistic(config)
    print(population)


if __name__ == '__main__':
    main()
