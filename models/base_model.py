#!/usr/bin/python3
"""
    BaseModel defines all common attributes/mmethods for
    other classes. """
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """ Base of all other classes """
    def __init__(self, *args, **kwargs):
        """ Initialization of a Base instance
        Args:
            - *args: list of arguments
            - **kwargs: dict of key-values arguments
        """

        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                            kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                            kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """ String representation """
        return f'[{type(self).__name__}] ({self.id}) {self.__dict__}'

    def save(self):
        """ Updates the public instance attribute updated_at with
            the current datetime"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """ Returns a dictionary containing all the key/values of
            the instance"""
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict
