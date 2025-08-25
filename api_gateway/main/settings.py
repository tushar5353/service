import os
import sys
from functools import lru_cache
from service.utils.config import Config

config_obj = Config()
config = config_obj.get_config("environment")["service"]

class Environment:
    environment: str = config["environment"]
    app_name: str = config["app_name"]
    app_port: int = config["app_port"]
    origins: list = config["origins"]
    server: str = config["server"]
    workers: int = config["workers"]
    reload: bool = config["reload"]

@lru_cache
def get_settings():
    """
    Function to return the settings'
    """
    settings = Environment()
    return settings
