import json
import os

class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        # load the config file and handle potential errors
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found at {self.config_path}")

        with open(self.config_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON: {e}")

    def get(self, key: str, default=None):
        # get a specific configuration value or return default
        return self.config.get(key, default)

    def set(self, key: str, value):
        # set a specific configuration value and save it
        self.config[key] = value
        self.save_config()

    def save_config(self):
        # save the current config back to the file
        with open(self.config_path, 'w') as file:
            json.dump(self.config, file, indent=4)

# example usage
if __name__ == '__main__':
    config_loader = ConfigLoader('config.json')
    print(config_loader.get('some_key', 'default_value'))  # change 'some_key' as needed
    # TODO: add more error handling and logging functionality