import pandas as pd
import folium

from src.config import Config
from src.utils import *
from src.visualisation import *
from src.population import *

def main():
    print("\t-- Loading config...\n")
    config = Config()

    # Data basic stat
    data = import_data(config)
    observe_data(data)

    # Create population
    population = Population()
    population.populate(data)
    print(population)

    print("\n\t-- Simulation ready.")

    # Visualisation

    plot_tree_population(population)


if __name__ == '__main__':
    main()
