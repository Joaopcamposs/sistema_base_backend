"""
Configurações de teste compartilhadas.
Este arquivo contém fixtures globais para todos os testes.
"""

import os
import pytest

# Define ambiente de teste antes de qualquer import
os.environ["TEST_ENV"] = "true"

# Registra os plugins de mocks
pytest_plugins = ["tests.mocks"]


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    """Define variáveis de ambiente para testes."""
    os.environ["TEST_ENV"] = "true"
    yield
