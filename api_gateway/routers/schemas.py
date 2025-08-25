from pydantic import BaseModel, validator
from typing import Literal, List, Union

from service.utils.custom_validators import \
        validate_api_key

class CustomBaseModel(BaseModel):
    def __init__(self, **data):
        super().__init__(**data)
        # If api_key field exists, validate it globally
        api_key = data.get("api_key")
        validate_api_key(api_key)

class TestTimeout(BaseModel):
    test_value: int

class AddUser(CustomBaseModel):
    api_key: str
    user_name: str
    email: str

class NewOrder(CustomBaseModel):
    api_key: str
    user_id: int
    product: str
    quantity: int
