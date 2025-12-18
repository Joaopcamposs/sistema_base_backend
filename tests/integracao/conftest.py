"""
Configuração específica para testes de integração.
Testes de integração precisam de banco de dados e conexões externas.
"""

import os
from typing import AsyncGenerator, Any
import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import text, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

# Define ambiente de teste
os.environ["TEST_ENV"] = "true"


@pytest.fixture(scope="session")
def event_loop():
    """Cria event loop para a sessão de testes."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Cria engine de teste."""
    from infra.banco_de_dados import obter_uri_do_banco_de_dados

    engine = create_async_engine(
        url=obter_uri_do_banco_de_dados(eh_teste=True),
        isolation_level="SERIALIZABLE",
        future=True,
        poolclass=NullPool,
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def setup_database(test_engine):
    """Cria todas as tabelas no banco de dados de teste."""
    from libs.ddd.adaptadores.orm.declarativo import Base

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture(scope="function")
async def limpar_banco_de_dados(test_engine, setup_database):
    """Limpa rapidamente todas as tabelas conhecidas no metadata."""
    from libs.ddd.adaptadores.orm.declarativo import Base

    async with test_engine.connect() as conn:
        tables = [f'"{table.name}"' for table in Base.metadata.sorted_tables]
        if tables:
            table_names = ", ".join(tables)
            stmt = text(f"TRUNCATE TABLE {table_names} RESTART IDENTITY CASCADE;")
            await conn.execute(stmt)
            await conn.commit()

    yield


@pytest_asyncio.fixture(scope="function")
async def mock_primeira_empresa(limpar_banco_de_dados) -> None:
    """Cria a primeira empresa e usuário de teste."""
    from infra.banco_de_dados.inicializadores import criar_primeira_empresa_e_usuario

    await criar_primeira_empresa_e_usuario()


@pytest_asyncio.fixture
async def client_async_api(mock_primeira_empresa) -> AsyncGenerator[AsyncClient, Any]:
    """Cliente HTTP assíncrono para testes de API."""
    from contextos_de_negocio.main import app
    from contextos_de_negocio.servicos.executores.seguranca import create_access_token
    from datetime import timedelta

    token = create_access_token(
        data={
            "email": "joao",
            "empresa_id": "7529b0ae-81ad-488b-b4ed-ecc094ca5084",
        },
        expires_delta=timedelta(minutes=15),
    )
    headers = {"Authorization": f"Bearer {token}"}
    client_api_test = AsyncClient(app=app, base_url="http://test", headers=headers)
    async with client_api_test as client:
        yield client
