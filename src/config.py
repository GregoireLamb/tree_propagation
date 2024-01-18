import json

import yaml
from pathlib import Path


class Config:
    def __init__(self):
        """
        Initialize Config class. Load config.yaml file and define paths.
        """
        # Define root directory, one level up from current directory
        self.root = Path(__file__).parent.parent
        self.config_path = f'{self.root}/config.yaml'

        self.__config = self.load_config()

        # Execution
        self.seed = self.__config["seed"]
        self.data_path = self.__config["data_path"]
        self.data_file = self.__config["data_file"]
        self.species_mapping_file = self.__config["species_mapping_file"]
        self.species_translation_file = self.__config["species_translation_file"]
        self.seed_amount_file = self.__config["seed_amount_file"]
        self.spreading_factors_file = self.__config["spreading_factors_file"]
        self.simulation_duration = self.__config["simulation_duration"]
        self.default_seeding_radius = self.__config["default_seeding_radius"]
        self.bounding_box = ((self.__config["vienna_bounding_box_lat1"], self.__config["vienna_bounding_box_long1"]),
                             (self.__config["vienna_bounding_box_lat2"],self.__config["vienna_bounding_box_long2"]))

        with open(self.data_path + self.seed_amount_file, "r", encoding="utf-8") as f:
            self.seed_amount_map = json.load(f)
            self.seed_amount_map = {int(k): v for k, v in self.seed_amount_map.items()}


    def load_config(self):
        """
        Load config.yaml file
        Returns:
            config (dict): Dictionary with config.yaml file
        """
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
