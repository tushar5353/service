from fastapi import HTTPException

from service.utils.config import Config

config_obj = Config()
env_config = config_obj.get_config("environment")

def validate_api_key(api_key):
    if api_key!=env_config["service"]["api_key"]:
        raise HTTPException(status_code=404, detail="Invalid API Key")
