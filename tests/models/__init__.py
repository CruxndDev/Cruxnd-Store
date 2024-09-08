import unittest

from app.models import generate_user_id


class TestUtilities(unittest.TestCase):

    def test_uuid(self):
        self.assertEqual(len(generate_user_id()), 36)