import json
import os

class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config_data = {}

    def load(self) -> dict:
        # check if the config file exists
        if not os.path.isfile(self.config_path):
            raise FileNotFoundError(f"Config file not found at {self.config_path}")

        with open(self.config_path, 'r') as file:
            try:
                self.config_data = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON: {e}")

        return self.config_data

    def get(self, key: str, default=None):
        # get a specific key from the loaded config
        return self.config_data.get(key, default)

# example usage
if __name__ == "__main__":
    # TODO: handle command line arguments for the config path
    config_loader = ConfigLoader("config.json")
    try:
        config = config_loader.load()
        print(config)
    except Exception as e:
        print(f"Failed to load config: {e}")