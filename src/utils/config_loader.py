import json
import os

class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        # check if the config file exists
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        
        # load the config file
        with open(self.config_path, 'r') as config_file:
            try:
                return json.load(config_file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON from config file: {e}")

    def get(self, key: str, default=None):
        # get a value from the config, return default if not found
        return self.config.get(key, default)

    def __getitem__(self, key: str):
        # allow dict-like access
        return self.get(key)

# example usage
if __name__ == "__main__":
    # TODO: update path to your config file
    config_loader = ConfigLoader('path/to/your/config.json')
    print(config_loader.get('some_key', 'default_value'))  # replace with your key