import json
import os

class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON: {e}")

    def get(self, key: str, default=None):
        return self.config_data.get(key, default)

# example usage
if __name__ == "__main__":
    config_loader = ConfigLoader('config.json')
    api_key = config_loader.get('api_key', 'default_key')
    print(f"Loaded API Key: {api_key}")  # TODO: remove this before production