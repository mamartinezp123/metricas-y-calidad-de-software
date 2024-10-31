import unittest

from src.main import User


class TestMain(unittest.TestCase):
    def test_instance_user_success(self):
        user = User("testuser", "password123", 15)
        self.assertEqual(user.secret, "password123")
