#!/usr/bin/python3
""" Module for FileStorage Class """

import json
import os

class FileStorage:
    """ Class for serialization and deserialization """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Returns the dictionary __objects """
        return FileStorage.__objects

    def new(self, obj):
        """ Sets new obj in __objects dictionary. """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """ Serializes __objects to the JSON file """
        try:
            with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
                data = {k:v.to_dict() for k, v in FileStorage.__objects.items()}
                json.dump(data, f)
        except (IOError, TypeError) as e:
            print(f"Error saving to file: {e}")

    def classes(self):
        """ Returns a dictionary of valid classes and their references """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
                "BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review,
                }
        return classes

    def reload(self):
        """" Deserializes the JSON file """
        if not os.path.isfile(FileStorage.__file_path):
            return

        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                obj_dict = json.load(f)
                obj_dict = {k: self.classes()[v["__class__"]](**v)
                        for k, v in obj_dict.items()}
                FileStorage.__objects = obj_dict

        except (FileNotFoundError, IOError, json.JSONDecodeError) as e:
            print(f"Error loading file: {e}")
