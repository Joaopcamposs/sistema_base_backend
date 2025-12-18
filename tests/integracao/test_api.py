"""
Testes de integração para os endpoints da API.
"""

import pytest
from uuid import uuid4
from httpx import AsyncClient

from tests.mocks import ID_EMPRESA_TESTE


@pytest.mark.asyncio
class TestAPIRoot:
    """Testes para o endpoint raiz."""

    async def test_deve_retornar_mensagem_api_no_ar(self, client_async_api: AsyncClient):
        """Deve retornar mensagem indicando que API está no ar."""
        response = await client_async_api.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "API está no ar!"}


@pytest.mark.asyncio
class TestAPIUsuario:
    """Testes para os endpoints de usuário."""

    async def test_deve_listar_usuarios(self, client_async_api: AsyncClient):
        """Deve listar usuários."""
        response = await client_async_api.get("/usuarios/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_deve_cadastrar_usuario(
        self, client_async_api: AsyncClient, cpf_valido
    ):
        """Deve cadastrar um novo usuário."""
        email_unico = f"api_user_{uuid4().hex[:8]}@teste.com"

        payload = {
            "nome": "Usuario API",
            "email": email_unico,
            "cpf": cpf_valido,
            "senha": "senha123",
            "ativo": True,
            "adm": False,
            "permissoes": ["leitura"],
        }

        response = await client_async_api.post("/usuarios/", json=payload)

        assert response.status_code in [200, 201]

    async def test_deve_retornar_erro_usuario_duplicado(
        self, client_async_api: AsyncClient, cpf_valido
    ):
        """Deve retornar erro ao cadastrar usuário com email duplicado."""
        email_unico = f"api_dup_{uuid4().hex[:8]}@teste.com"

        payload = {
            "nome": "Usuario Duplicado",
            "email": email_unico,
            "cpf": cpf_valido,
            "senha": "senha123",
            "ativo": True,
            "adm": False,
            "permissoes": [],
        }

        # Primeiro cadastro
        response1 = await client_async_api.post("/usuarios/", json=payload)
        assert response1.status_code in [200, 201]

        # Segundo cadastro com mesmo email
        payload["cpf"] = "52998224725"  # CPF diferente
        response2 = await client_async_api.post("/usuarios/", json=payload)
        assert response2.status_code == 409  # Conflict


@pytest.mark.asyncio
class TestAPICliente:
    """Testes para os endpoints de cliente."""

    async def test_deve_listar_clientes(self, client_async_api: AsyncClient):
        """Deve listar clientes."""
        response = await client_async_api.get("/clientes/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_deve_cadastrar_cliente(
        self, client_async_api: AsyncClient, cpf_valido
    ):
        """Deve cadastrar um novo cliente."""
        email_unico = f"api_cli_{uuid4().hex[:8]}@teste.com"

        payload = {
            "nome": "Cliente API",
            "cpf": cpf_valido,
            "telefone": "11999999999",
            "telefone_2": "",
            "email": email_unico,
            "cep": "01310100",
            "rua": "Avenida Paulista",
            "numero": "1000",
            "complemento": "Sala 101",
            "bairro": "Bela Vista",
            "cidade": "São Paulo",
            "estado": "SP",
            "pais": "Brasil",
        }

        response = await client_async_api.post("/clientes/", json=payload)

        assert response.status_code in [200, 201]


@pytest.mark.asyncio
class TestAPIEmpresa:
    """Testes para os endpoints de empresa."""

    async def test_deve_consultar_empresa(self, client_async_api: AsyncClient):
        """Deve consultar empresa atual."""
        response = await client_async_api.get(f"/empresas/{ID_EMPRESA_TESTE}")

        # Pode retornar 200 se encontrar ou 404 se não encontrar
        assert response.status_code in [200, 404]


@pytest.mark.asyncio
class TestAPIServico:
    """Testes para os endpoints de serviço."""

    async def test_deve_listar_servicos(self, client_async_api: AsyncClient):
        """Deve listar serviços."""
        response = await client_async_api.get("/servicos/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_deve_cadastrar_servico(self, client_async_api: AsyncClient):
        """Deve cadastrar um novo serviço."""
        codigo_unico = f"SRV_{uuid4().hex[:8]}"

        payload = {
            "codigo": codigo_unico,
            "nome": "Servico API",
            "descricao": "Descrição do serviço",
            "valor": 150.00,
            "ativo": True,
        }

        response = await client_async_api.post("/servicos/", json=payload)

        assert response.status_code in [200, 201]
