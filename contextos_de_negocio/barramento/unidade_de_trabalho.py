from __future__ import annotations

import libs.ddd.adaptadores.orm.declarativo  # isso garante que todos os módulos sejam carregados
from typing import Generic, TypeVar, Callable

from sqlalchemy.orm import DeclarativeBase
from barramento_de_mensagens.unidade_de_trabalho import UnidadeDeTrabalhoBase

from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from infra.banco_de_dados import DEFAULT_SQL_SESSION_FACTORY, get_sql_engine
from libs.ddd.adaptadores.orm.declarativo import Base
from libs.ddd.adaptadores.repositorio.repositorio import (
    RepositorioDominio,
    RepositorioConsulta,
)

REPO_LEITURA = TypeVar("REPO_LEITURA")
REPO_ESCRITA = TypeVar("REPO_ESCRITA")


class UnidadeDeTrabalho(UnidadeDeTrabalhoBase, Generic[REPO_ESCRITA, REPO_LEITURA]):
    domain_repo: RepositorioDominio
    view_repo: RepositorioConsulta

    def __init__(
        self,
        session_factory: Callable = DEFAULT_SQL_SESSION_FACTORY,  # <== defina um session factory padrão
        engine_factory: Callable = get_sql_engine,  # <== defina um engine factory padrão
        base: type[DeclarativeBase] = Base,  # <== defina um base padrão
        usuario: UsuarioEntidade | None = None,
        schema: str | None = None,
        somente_leitura: bool = False,
        criar_schema: bool = False,
    ):
        self.somente_leitura = somente_leitura
        self.engine_factory = engine_factory
        self.base = base

        super().__init__(
            session_factory=session_factory,
            engine_factory=engine_factory,
            base=base,
            usuario=usuario,
            schema=schema,
            criar_schema=criar_schema,
        )
