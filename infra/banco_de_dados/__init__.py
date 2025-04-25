import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    AsyncConnection,
)

from libs.ddd.adaptadores.orm.declarativo import Base
from libs.utils.constantes import (
    DB_HOST,
    DB_PASSWORD,
    DB_USER,
    DB_NAME,
)

engine: AsyncEngine | None = None


def obter_uri_do_banco_de_dados(eh_teste: bool = False) -> str:
    ambiente_de_teste = eh_teste or os.getenv("TEST_ENV")
    em_docker = os.getenv("IN_DOCKER", "false").lower() == "true"

    host = DB_HOST
    port = 5432 if any([ambiente_de_teste, em_docker]) else 54322
    password = DB_PASSWORD
    user = DB_USER
    db_name = DB_NAME
    database_uri = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"

    return database_uri


def obter_uri_do_celery() -> str:
    # Verifica se foi definido que está em ambiente Docker
    em_docker = os.getenv("IN_DOCKER", "false").lower() == "true"

    host_celery = "redis" if em_docker else "localhost"
    celery_uri = f"redis://{host_celery}:6379/0"

    return celery_uri


async def set_schema_name(session: AsyncSession, schema: str):
    await session.execute(text(f'SET search_path TO "{schema}"'))
    setattr(session, "schema", str(schema))


def get_schema_name(session: AsyncSession):
    return getattr(session, "schema", "public")


def get_sql_engine(
    isolation_level: str = "READ COMMITTED",
    force_create_engine: bool = False,
) -> AsyncEngine:
    def _criar_engine_correta():
        global engine

        if force_create_engine:
            engine_replica = create_async_engine(
                obter_uri_do_banco_de_dados(),
                isolation_level=isolation_level,
                future=True,
            )
            return engine_replica

        if not engine:
            engine = create_async_engine(
                obter_uri_do_banco_de_dados(),
                isolation_level=isolation_level,
                future=True,
            )
        return engine

    engine_correta = _criar_engine_correta()

    return engine_correta


async def DEFAULT_SQL_SESSION_FACTORY(
    somente_leitura: bool,
    schema: str | None = None,
    isolation_level: str = "READ COMMITTED",
) -> AsyncSession:
    """
    Cria uma sessão SQLAlchemy, somente leitura ou não, com o esquema especificado.
    Deve ser utilizada internamente em estruturas que lidam com contextos, como a UnidadeDeTrabalho.
    """
    _engine = get_sql_engine(isolation_level=isolation_level)

    schema_atual = schema or "public"
    execution_options = dict(schema_translate_map={None: schema_atual})

    if somente_leitura:
        execution_options["isolation_level"] = "AUTOCOMMIT"

    session = AsyncSession(
        bind=_engine.execution_options(**execution_options),
        autoflush=True,
        expire_on_commit=False,
    )
    await set_schema_name(session, schema_atual)

    async def async_close():
        await session.close()

    # Anexa o métodu async para ser usado explicitamente
    session.async_close = async_close  # type: ignore[attr-defined]

    return session


@asynccontextmanager
async def get_session(
    somente_leitura: bool, schema: str = "public"
) -> AsyncGenerator[AsyncSession, None]:
    """
    Gerenciador de contexto para facilitar o uso da funcao que cria a sessao.
    Deve ser usada em contexto abertos diretamente, sem uso da unidade de trabalho.
    Não deve ser usada para substituir a função principal dentro da unidade de trabalho.
    """
    session = await DEFAULT_SQL_SESSION_FACTORY(
        somente_leitura=somente_leitura, schema=schema
    )
    try:
        yield session
    finally:
        await session.close()


SCHEMAS_PARA_NAO_LISTAR: tuple[str, ...] = (
    "public",
    "information_schema",
    "pg_catalog",
    "pg_toast",
)


async def listar_schemas_existentes() -> list[str]:
    async with get_sql_engine().begin() as conn:
        result = await conn.execute(
            text("SELECT schema_name FROM information_schema.schemata")
        )
        return [row[0] for row in result if row[0] not in SCHEMAS_PARA_NAO_LISTAR]


async def verificar_schema_existente(conn: AsyncConnection, schema_id: str) -> None:
    result = await conn.execute(
        text(
            f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema_id}'"
        )
    )
    if result.fetchone():
        raise ValueError(f"Schema {schema_id} já existe")


async def excluir_schema(schema_id: str) -> None:
    async with get_sql_engine().begin() as conn:
        await conn.execute(text(f'DROP SCHEMA "{schema_id}" CASCADE;'))


async def criar_schema_e_tabelas(schema_id: str):
    """
    1. Cria o schema no Postgres
    2. Ajusta os metadados para usar schema_id
    3. Cria as tabelas do tenant dentro dele
    4. Restaura schema=None nos metadados
    """
    # criar engine temporária
    engine_temp: AsyncEngine = get_sql_engine(force_create_engine=True)

    # 1) criar schema
    async with engine_temp.begin() as conn:
        await verificar_schema_existente(conn, schema_id)
        await conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema_id}"'))

    # 2) atribuir schema nos objetos
    for table in Base.metadata.sorted_tables:
        if table.schema != "public":
            table.schema = schema_id

    # 3) criar tabelas no novo schema
    async with engine_temp.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # fechar a engine temporária
    await engine_temp.dispose()

    # 4) restaurar esquema padrão (public)
    for table in Base.metadata.sorted_tables:
        if table.schema != "public":
            table.schema = None
