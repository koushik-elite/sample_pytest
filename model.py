import pytest
import requests as requests
from pydantic.v1 import BaseModel

class User(BaseModel):
    """Model for our users"""
    id: str
    name: str
    email: str
    password: str

    def sign_up(self):
        """Wow, we can add methods too!"""
        pass