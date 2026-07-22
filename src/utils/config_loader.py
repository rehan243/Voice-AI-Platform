import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        
        with open(self.config_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.config[key] = value
        self.save_config()

    def save_config(self) -> None:
        with open(self.config_path, 'w') as file:
            json.dump(self.config, file, indent=4)

# usage example
if __name__ == "__main__":
    config_loader = ConfigLoader('config.json')
    print(config_loader.get('some_key', 'default_value'))  # TODO: replace with actual key
    config_loader.set('new_key', 'new_value')  # TODO: update with real values to test