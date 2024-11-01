import unittest
from unittest.mock import patch
from flask import json
from flask_jwt_extended import create_access_token

from src.main import app, System, User, is_not_blank, is_adult


class UserSystemTestCase(unittest.TestCase):
    def setUp(self):
        """Configura el entorno antes de cada prueba."""
        self.system = System()
        self.user_name = "TestUser"
        self.user_secret = "secret123"
        self.user_age = 25

    def test_add_user(self):
        """Prueba que un usuario se agregue correctamente."""
        user = self.system.add_user(self.user_name, self.user_secret, self.user_age)
        self.assertIn(user, self.system.get_users())
        self.assertEqual(user.name, self.user_name)
        self.assertEqual(user.secret, self.user_secret)
        self.assertEqual(user.age, self.user_age)

    def test_login_user_success(self):
        """Prueba de inicio de sesión exitoso."""
        self.system.add_user(self.user_name, self.user_secret, self.user_age)
        result = self.system.login_user(self.user_name, self.user_secret)
        self.assertTrue(result)

    def test_login_user_failure(self):
        """Prueba de inicio de sesión fallido."""
        result = self.system.login_user("WrongUser", "wrongSecret")
        self.assertFalse(result)

    def test_delete_user(self):
        """Prueba de eliminación de un usuario existente."""
        self.system.add_user(self.user_name, self.user_secret, self.user_age)
        self.system.delete_user(self.user_name)
        self.assertNotIn(self.user_name, [user.name for user in self.system.get_users()])

    def test_is_adult(self):
        """Prueba la función is_adult para verificar si un usuario es adulto."""
        self.assertTrue(is_adult(18))
        self.assertFalse(is_adult(17))

    def test_is_not_blank(self):
        """Prueba la función is_not_blank para verificar entradas vacías o None."""
        self.assertTrue(is_not_blank(""))
        self.assertTrue(is_not_blank(None))
        self.assertFalse(is_not_blank("Non-empty string"))


class UserBlueprintTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura la aplicación Flask para pruebas y JWT."""
        cls.app = app
        cls.app.config["TESTING"] = True
        cls.app.config["WTF_CSRF_ENABLED"] = False  # Deshabilita CSRF para pruebas
        cls.client = cls.app.test_client()

    @patch('src.main.System.add_user')
    def test_create_user(self, mock_add_user):
        """Prueba la creación de usuario a través de la ruta /users."""
        mock_add_user.return_value = User("TestUser", "secret123", 25)
        response = self.client.post('/users', json={
            "name": "TestUser",
            "secret": "secret123",
            "age": 25
        })
        self.assertEqual(response.status_code, 201)

    @patch('src.main.System.login_user')
    def test_login_user_success(self, mock_login_user):
        """Prueba de inicio de sesión exitoso a través de la ruta /users/login."""
        mock_login_user.return_value = True
        response = self.client.post('/users/login', json={
            "name": "TestUser",
            "secret": "secret123"
        }, headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", json.loads(response.data))

    def test_login_user_failure(self):
        """Prueba de inicio de sesión fallido a través de la ruta /users/login."""
        response = self.client.post('/users/login', json={
            "name": "WrongUser",
            "secret": "wrongSecret"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid credentials", response.get_json().get("menssage"))

    def test_get_users(self):
        """Prueba para la ruta /users con token de acceso JWT."""
        with self.app.test_request_context():
            access_token = create_access_token(identity="test_user")
            headers = {"Authorization": f"Bearer {access_token}"}
            response = self.client.get('/users', headers=headers)
            self.assertEqual(response.status_code, 200)

    def test_user(self):
        user = User("Test", "test", 18)
        user.print_age(18)
        user.print_name("Test")
        user.print_secret("test")
        self.assertEqual("Test", user.get_name())
        self.assertEqual("test", user.get_secret())
        self.assertEqual(18, user.get_age())


if __name__ == "__main__":
    unittest.main()
