#!/usr/bin/python3
""" Review Model """
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class that inherits from BaseModel
    """
    # Public class attributes
    place_id = ""
    user_id = ""
    text = ""
