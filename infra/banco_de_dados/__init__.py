import os
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

from libs.utils.constantes import (
    DB_HOST,
    DB_PASSWORD,
    DB_USER,
    DB_NAME,
    EMAIL_PRIMEIRO_USUARIO,
    SENHA_PRIMEIRO_USUARIO,
    CPF_PRIMEIRO_USUARIO,
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


def DEFAULT_SQL_SESSION_FACTORY(
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
    # await set_schema_name(session, schema)

    async def async_close():
        await session.close()

    # Anexa o métodu async para ser usado explicitamente
    session.async_close = async_close  # type: ignore[attr-defined]

    return session


async def criar_primeiro_usuario(id_empresa: UUID) -> None:
    from sqlalchemy import select, insert
    from contextos_de_negocio.adaptadores.orm.declarativo.usuario import UsuarioDB
    from uuid import uuid4
    from contextos_de_negocio.dominio.agregados.usuario import Usuario
    from libs.utils.tipos_basicos import CPF

    async with DEFAULT_SQL_SESSION_FACTORY(somente_leitura=False) as session:
        usuarios = (await session.execute(select(UsuarioDB).filter_by())).scalars().all()

        if not usuarios:
            senha_criptografada = Usuario.criptografar_senha(SENHA_PRIMEIRO_USUARIO)
            dados = {
                "id": uuid4(),
                "empresa_id": id_empresa,
                "nome": "Admin",
                "email": EMAIL_PRIMEIRO_USUARIO,
                "cpf": CPF_PRIMEIRO_USUARIO,
                "senha": senha_criptografada,
                "adm": True,
                "ativo": True,
                "permissoes": [],
                "criado_por": None,
                "criado_em": None,
                "modificado_por": None,
                "ultima_modificacao_em": None,
                "deletado_por": None,
                "deletado_em": None,
            }
            await session.execute(insert(UsuarioDB).values(dados))
            await session.commit()


async def criar_primeira_empresa() -> UUID | None:
    from sqlalchemy import select, insert
    from uuid import uuid4
    from contextos_de_negocio.adaptadores.orm.declarativo.empresa import EmpresaDB

    async with DEFAULT_SQL_SESSION_FACTORY(somente_leitura=False) as session:
        empresas = (await session.execute(select(EmpresaDB).filter_by())).scalars().all()

        if not empresas:
            id_empresa = uuid4()
            dados = {
                "id": id_empresa,
                "razao_social": "JP ADM",
                "nome_fantasia": "JP ADM",
                "nome_responsavel": "João Campos",
                "email": EMAIL_PRIMEIRO_USUARIO,
                "cpf": CPF_PRIMEIRO_USUARIO,
                "cnpj": None,
                "ativo": True,
                "criado_por": None,
                "criado_em": None,
                "modificado_por": None,
                "ultima_modificacao_em": None,
                "deletado_por": None,
                "deletado_em": None,
            }
            await session.execute(insert(EmpresaDB).values(dados))
            await session.commit()

            return id_empresa

        return None


async def criar_primeira_empresa_e_usuario() -> None:
    id_empresa = await criar_primeira_empresa()

    if id_empresa:
        await criar_primeiro_usuario(id_empresa)
