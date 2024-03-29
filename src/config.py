import json

import yaml
from pathlib import Path


class Config:
    def __init__(self):
        """
        Initiamlize Config class. Load config.yal file and define paths.
        """
        # Define root directory, one level up from current directory
        self.root = Path(__file__).parent.parent
        self.config_path = f'{self.root}/config.yaml'

        self.__config = self.load_config()

        # Execution
        self.seed = self.__config["seed"]
        self.show_plot_on_the_fly = self.__config["show_plot_on_the_fly"]
        self.data_path = self.__config["data_path"]
        self.data_file = self.__config["data_file"]
        self.result_path = self.__config["result_path"]
        self.wind_strategy = self.__config["wind_strategy"]
        self.tree_size_visualization_max = self.__config["tree_size_visualization_max"]
        self.tree_size_visualization_min = self.__config["tree_size_visualization_min"]
        self.species_label_mapping_file = self.__config["species_label_mapping_file"]
        self.species_mapping_file = self.__config["species_mapping_file"]
        self.species_translation_file = self.__config["species_translation_file"]
        self.seed_amount_file = self.__config["seed_amount_file"]
        self.spreading_factors_file = self.__config["spreading_factors_file"]
        self.simulation_duration = self.__config["simulation_duration"]
        self.default_seeding_radius = self.__config["default_seeding_radius"]
        self.seed_living_space = self.__config["seed_living_space"]
        self.bounding_box = ((self.__config["vienna_bounding_box_lat1"], self.__config["vienna_bounding_box_long1"]),
                             (self.__config["vienna_bounding_box_lat2"],self.__config["vienna_bounding_box_long2"]))
        if self.wind_strategy == "constant":
            self.wind_strength = self.__config["wind_strength"]
            self.wind_direction = self.__config["wind_direction"]

        with open(self.data_path + self.seed_amount_file, "r", encoding="utf-8") as f:
            self.seed_amount_map = json.load(f)
            self.seed_amount_map = {int(k): v for k, v in self.seed_amount_map.items()}

        with open(self.data_path + self.species_label_mapping_file, "r", encoding="utf-8") as f:
            species_label_map = json.load(f)
            self.species_label_map = {int(k): v for k, v in species_label_map.items()}


    def load_config(self):
        """
        Load config.yaml file
        Returns:
            config (dict): Dictionary with config.yaml file
        """
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
