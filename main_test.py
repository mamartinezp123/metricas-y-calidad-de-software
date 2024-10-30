import pytest
from main import Sistema


def test_agregar_usuario():
    sistema = Sistema()
    sistema.agregar_usuario("testuser", "password123")
    assert len(sistema.usuarios) == 1
