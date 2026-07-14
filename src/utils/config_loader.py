import json
import os
from typing import Any, Optional

class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = {}

    def load(self) -> dict:
        """load configuration from the specified file"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found at: {self.config_path}")
        
        try:
            with open(self.config_path, 'r') as file:
                self.config = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from config file: {self.config_path}") from e
        
        return self.config

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """get a value from the config by key"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """set a value in the config and save it"""
        self.config[key] = value
        self._save()

    def _save(self) -> None:
        """save the current config to the file"""
        try:
            with open(self.config_path, 'w') as file:
                json.dump(self.config, file, indent=4)
        except IOError as e:
            raise IOError(f"Failed to save config to {self.config_path}") from e

# example usage
if __name__ == "__main__":
    config_loader = ConfigLoader("config.json")
    try:
        config = config_loader.load()
        print("Loaded config:", config)
    except (FileNotFoundError, ValueError) as e:
        print(e)
    # TODO: add more functionality or validations as needed