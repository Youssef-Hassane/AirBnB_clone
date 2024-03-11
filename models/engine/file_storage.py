#!/usr/bin/python3
import json
from os.path import isfile


class FileStorage:
    """ FileStorage class """

    # Private Class Attributes
    __file_path = "file.json"
    __objects = {}

    # Public Instance Methods
    def all(self):
        """
        Public instance methods that returns the dictionary __objects
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Public instance methods that sets in
        __objects the obj with key <obj class name>.id
        """
        FileStorage.__objects[
            "{}.{}".format(obj.__class__.__name__, obj.id)
        ] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        serialized_objs = {}
        for key, obj in self.__objects.items():
            serialized_objs[key] = obj.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(serialized_objs, file, indent=4)

    def reload(self):
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        """
        Public instance method that deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists ; otherwise, do nothing.
        If the file doesn’t exist, no exception should be raised)
        """

        if not isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r") as file:
            obj_dict = json.load(file)
            classes = {
                "BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review,
            }
            obj_dict = {
                key: classes[value["__class__"]](**value)
                for key, value in obj_dict.items()
            }
            FileStorage.__objects = obj_dict
