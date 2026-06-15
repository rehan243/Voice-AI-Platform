import json
import os

class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self):
        if not os.path.isfile(self.config_path):
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON: {e}")

    def get(self, key: str, default=None):
        return self.config_data.get(key, default)

    def set(self, key: str, value):
        self.config_data[key] = value
        self.save_config()

    def save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config_data, f, indent=4)

# example usage
if __name__ == '__main__':
    config_loader = ConfigLoader('path/to/config.json')  # TODO: update path as needed
    print(config_loader.get('some_key', 'default_value'))