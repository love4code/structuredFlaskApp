import unittest
from app.models import User

# Creating test to test our password hashing


class UserModelTestCase(unittest.TestCase):

    def test_password_setter(self):
        """Verify Password Hash is working correctly"""
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        """Run a test to throw an error if tried to access attribute
        password """
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        """Verify password check"""
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)