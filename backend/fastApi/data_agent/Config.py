import configparser


class Config:
    """Handles loading and accessing configuration from an INI file."""
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get(self, section, key):
        """Retrieve the configuration value for a given section and key."""
        return self.config.get(section, key)