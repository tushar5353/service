from pydantic import BaseModel, validator
from typing import Literal, List, Union

from service.utils.custom_validators import \
        validate_api_key

class TestTimeout(BaseModel):
    test_value: int

class AddUser(BaseModel):
    api_key: str
    user_name: str
    email: str
    api_key_validator: validate_api_keu(api_key)

class NewOrder(BaseModel):
    api_key: str
    user_id: int
    product: str
    quantity: int
    api_key_validator: validate_api_keu(api_key)
