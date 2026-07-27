import json
import os

class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config_data = {}

    def load(self) -> dict:
        # load json config file
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        
        with open(self.config_path, 'r') as file:
            self.config_data = json.load(file)
        
        return self.config_data

    def get(self, key: str, default=None):
        # get a specific config value
        return self.config_data.get(key, default)

    def set(self, key: str, value):
        # set a config value (not saving it yet)
        self.config_data[key] = value

    def save(self):
        # save updated config back to file
        with open(self.config_path, 'w') as file:
            json.dump(self.config_data, file, indent=4)

# example usage
if __name__ == "__main__":
    config_loader = ConfigLoader('config.json')
    try:
        config = config_loader.load()
        print("Loaded config:", config)
    except FileNotFoundError as e:
        print(e)
        # TODO: handle missing config more gracefully