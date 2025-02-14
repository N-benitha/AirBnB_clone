#!/usr/bin/python3
""" Unittest module for User Class """

import unittest
from datetime import datetime
import time
from models.user import User
import re
import json
from models.engine.file_storage import FileStorage
import os
from models import storage
from models.base_model import BaseModel


class Test_User(unittest.TestCase):

    """ Test Cases for the User Class """

    def setup(self):
        """Sets up test methods"""
        pass

    def tearDown(self):
        """ Tears down test methods """
        self.resetStorage()
        pass

    def resetStorage(self):
        """ Resets FileStorage data. """
        FileStorage.__FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_8_instatiation(self):
        """ Tests instatiantiation of User class. """

        b = User()
        self.assertEqual(str(type(b)), "<class 'models.user.User'>")
        self.assretIsInstance(b, User)
        self.assertTrue(issubclass((b), BaseModel))

    def test_8_attributes(self):
        """ Tests the attributes of User class. """
        attributes = storage.attributes()["User"]
        o = User()
        for k, v in attributes.items():
            self.assertTrue(hasattr(o, k))
            self.assertEqual(type(getattr(o, k, None)), v)


if __name__ == "__main__":
    unittest.main()
