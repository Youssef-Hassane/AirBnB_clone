#!/usr/bin/python3
"""Initializes the package"""
# import file_storage.py
from models.engine.file_storage import FileStorage as FS
# create the variable storage, an instance of FileStorage
storage = FS()
# call reload() method on this variable
storage.reload()
