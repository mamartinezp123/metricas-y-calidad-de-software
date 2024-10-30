import unittest
from src.main import Sistema


class TestMain(unittest.TestCase):
    def test_agregar_usuario(self):
        sistema = Sistema()
        sistema.agregar_usuario("testuser", "password123")
        self.assertEqual(len(sistema.usuarios), 1)
