import json
import os

class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = {}

    def load(self) -> dict:
        # check if the file exists
        if not os.path.isfile(self.config_path):
            raise FileNotFoundError(f"Config file not found at {self.config_path}")

        # read the json file
        with open(self.config_path, 'r') as file:
            self.config = json.load(file)

        return self.config

    def get(self, key: str, default=None):
        # get a config value with a default fallback
        return self.config.get(key, default)

    def set(self, key: str, value) -> None:
        # set a config value
        self.config[key] = value

    def save(self) -> None:
        # save config back to file
        with open(self.config_path, 'w') as file:
            json.dump(self.config, file, indent=4)

# TODO: add support for environment variable overrides
# can be handy to tweak settings without changing files