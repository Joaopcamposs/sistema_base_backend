"""
Configuração específica para testes unitários.
Testes unitários não precisam de banco de dados ou conexões externas.
"""

import os

# Define ambiente de teste
os.environ["TEST_ENV"] = "true"
