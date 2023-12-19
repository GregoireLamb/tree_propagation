import random

import matplotlib.pyplot as plt
import pandas as pd

from src.config import Config
from src.utils import *
from src.visualisation import *
from src.population import *

def main():
    print("\t-- Loading config...\n")
    config = Config()
    random.seed(config.seed)

    # Data basic stat
    data = import_data(config)
    observe_data(data)

    # Create population
    population = Population()
    population.populate(data)
    create_tree_map(population)
    print(population)

    print("\n\t-- Simulation ready.")

    run_simulation(population, config)
    print(population)

    create_tree_map(population)
    population.plot_statistic()
    # TODO save simulation results

if __name__ == '__main__':
    main()
