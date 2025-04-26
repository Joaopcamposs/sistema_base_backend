from __future__ import annotations

from typing import Generic, TypeVar

from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from infra.banco_de_dados import criar_schema_completo_dentro_de_uma_transacao
from libs.ddd.adaptadores.repositorio.repositorio import (
    RepositorioDominio,
    RepositorioConsulta,
)
from libs.ddd.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)

REPO_LEITURA = TypeVar("REPO_LEITURA")
REPO_ESCRITA = TypeVar("REPO_ESCRITA")


class UnidadeDeTrabalho(UnidadeDeTrabalhoAbstrata, Generic[REPO_ESCRITA, REPO_LEITURA]):
    domain_repo: RepositorioDominio
    view_repo: RepositorioConsulta

    def __init__(
        self,
        usuario: UsuarioEntidade | None = None,
        schema: str | None = None,
        somente_leitura: bool = False,
        criar_schema: bool = False,
    ):
        self.somente_leitura = somente_leitura

        super().__init__(
            usuario=usuario,
            schema=schema,
            criar_schema=criar_schema,
        )

    async def __aenter__(self) -> UnidadeDeTrabalho:
        self.commited = False

        if self.criar_schema:
            self.session = await criar_schema_completo_dentro_de_uma_transacao(
                schema_id=self.schema, session_factory=self.sql_session_factory
            )
            self.criar_schema = False
        else:
            self.session = await self.sql_session_factory(
                somente_leitura=False,
                schema=self.schema,
            )
        self.session_leitura = await self.sql_session_factory(
            somente_leitura=True, schema=self.schema
        )

        if not self.somente_leitura and self.domain_repo_class:
            self.domain_repo = self.domain_repo_class(self.session)

        if self.view_repo_class:
            self.view_repo = self.view_repo_class(self.session_leitura)

        return await super().__aenter__()  # type: ignore[return-value]

    async def __aexit__(  # type: ignore[override]
        self, *args: tuple[type[Exception], Exception, Exception]
    ) -> None:
        await super().__aexit__(*args)
