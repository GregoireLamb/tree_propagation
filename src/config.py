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
        self.simulation_duration = self.__config["simulation_duration"]

    def load_config(self):
        """
        Load config.yaml file
        Returns:
            config (dict): Dictionary with config.yaml file
        """
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
