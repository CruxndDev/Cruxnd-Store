import os, sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # * Adding the tests to the app path

from app.models import generate_user_id


class TestUtilities(unittest.TestCase):

    def test_uuid(self):
        self.assertEqual(len(generate_user_id()), 36)