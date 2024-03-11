#!/usr/bin/python3
""" City Model """
from models.base_model import BaseModel


class City(BaseModel):
    """
    City class that inherits from BaseModel
    """
    # Public class attributes
    state_id = ""
    name = ""
