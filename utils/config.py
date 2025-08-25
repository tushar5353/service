"""
Contains the operation related to fetching the configuration
as per environment. It will try to fetch the config from the
directory which is same as that of environment variable ENVIRONMENT
"""
import os
import yaml
from yaml.loader import SafeLoader
import logging

class Config:
    """
    A class to handle the config
    """
    def __init__(self):
        """
        Class' Constructor
        app_config_map is a dictionary containing the configuration
        file mappings for different Config Items
        """
        self.ENVIRONMENT = os.environ["ENVIRONMENT"]
        self.config_map = \
                {"db_migrations": "db_migrations.yaml",
                 "environment": "env.yaml"}

    def get_config(self, config_item):
        """
        Function to return the configuration for an app
        :param config_item: `str` - name of the config_item
        :return data: `dict` - application's config
        :raises: "Invalid Config Item"
        """
        logging.info(f"Getting config::{config_item}")
        self._is_valid_config_item(config_item)
        current_path = os.path.dirname(__file__)
        with open(f"{current_path}/../config/{self.ENVIRONMENT}/{self.config_map[config_item]}") as f:
            data = yaml.load(f, Loader=SafeLoader)
            return data

    def _is_valid_config_item(self, config_item):
        """
        helper function to validate the app's name
        :param config_item: `str` - config item's name
        """
        if config_item not in self.config_map.keys():
            raise Exception("Invalid Config Item")
        else:
            pass
