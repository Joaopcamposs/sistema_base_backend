import os
from typing import AsyncGenerator, Any

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from contextos_de_negocio.main import app
from infra.banco_de_dados import obter_uri_do_banco_de_dados
from libs.ddd.adaptadores.orm.declarativo import Base

pytest_plugins = ["tests.mocks"]


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    os.environ["TEST_ENV"] = "true"
    yield


@pytest_asyncio.fixture(scope="function", autouse=True)
async def mock_primeira_empresa() -> None:
    from infra.banco_de_dados.inicializadores import criar_primeira_empresa_e_usuario

    await criar_primeira_empresa_e_usuario()


@pytest_asyncio.fixture
async def client_async_api() -> AsyncGenerator[AsyncClient, Any]:
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


def test_engine():
    engine = create_async_engine(
        url=obter_uri_do_banco_de_dados(eh_teste=True),
        isolation_level="SERIALIZABLE",
        future=True,
    )
    return engine


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with test_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture(scope="function", autouse=True)
async def limpar_banco_de_dados():
    """Limpa rapidamente todas as tabelas conhecidas no metadata."""

    async with test_engine().connect() as conn:
        tables = [f'"{table.name}"' for table in Base.metadata.sorted_tables]
        if tables:
            table_names = ", ".join(tables)
            stmt = text(f"TRUNCATE TABLE {table_names} RESTART IDENTITY CASCADE;")
            await conn.execute(stmt)
            await conn.commit()

    yield
