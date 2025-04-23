import os

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

from libs.utils.constantes import DB_HOST, DB_PASSWORD, DB_USER, DB_NAME

engine: AsyncEngine | None = None


def obter_uri_do_banco_de_dados(eh_teste: bool = False) -> str:
    ambiente_de_teste = eh_teste or os.getenv("TEST_ENV")
    em_docker = os.getenv("IN_DOCKER", "false").lower() == "true"

    host = DB_HOST
    port = 5432 if not any([ambiente_de_teste, em_docker]) else 54322
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


async def set_schema_name(
    session: AsyncSession, schema: str, force_search_path: bool = False
):
    if force_search_path:
        await session.execute(text(f'SET search_path TO "{schema}"'))

    setattr(session, "schema", str(schema))


def get_schema_name(session: AsyncSession):
    return getattr(session, "schema", "public")


def get_sql_engine(
    isolation_level: str = "READ COMMITTED",
) -> AsyncEngine:
    global engine

    if not engine:
        engine = create_async_engine(
            obter_uri_do_banco_de_dados(),
            isolation_level=isolation_level,
            future=True,
        )

    return engine


async def DEFAULT_SQL_SESSION_FACTORY(
    somente_leitura: bool,
    schema: str = "public",
    isolation_level: str = "READ COMMITTED",
) -> AsyncSession:
    _engine = get_sql_engine(isolation_level=isolation_level)

    execution_options = dict(schema_translate_map={None: "public"})

    if somente_leitura:
        execution_options["isolation_level"] = "AUTOCOMMIT"

    session = AsyncSession(
        bind=_engine.execution_options(**execution_options),
        autoflush=True,
        expire_on_commit=False,
    )
    await set_schema_name(session, schema)

    async def _decorator_close(func: callable):
        """Decorator para fechar a conexão da engine ao fechar a sessão"""

        async def _inner(*args, **kwargs):
            func(*args, **kwargs)
            await _engine.dispose()

        return _inner

    session.close = await _decorator_close(session.close)

    return session
