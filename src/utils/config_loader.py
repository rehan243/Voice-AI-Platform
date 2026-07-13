import json
import os

class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = {}

    def load(self) -> dict:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found at: {self.config_path}")
        
        with open(self.config_path, 'r') as file:
            self.config = json.load(file)
        
        return self.config

    def get(self, key: str, default=None):
        return self.config.get(key, default)

    def set(self, key: str, value):
        self.config[key] = value
        self._save()

    def _save(self):
        with open(self.config_path, 'w') as file:
            json.dump(self.config, file, indent=4)

# example usage
if __name__ == "__main__":
    config_loader = ConfigLoader("config.json")
    try:
        config = config_loader.load()
        print("Loaded config:", config)
    except FileNotFoundError as e:
        print(e)
    # TODO: add more functionality or validations as needed