from __future__ import annotations

from typing import Generic

from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from libs.ddd.adaptadores.repositorio.repositorio import (
    RepositorioDominio,
    RepositorioConsulta,
)
from libs.ddd.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
    REPO_ESCRITA,
    REPO_LEITURA,
)


class UnidadeDeTrabalho(UnidadeDeTrabalhoAbstrata, Generic[REPO_ESCRITA, REPO_LEITURA]):
    domain_repo: RepositorioDominio
    view_repo: RepositorioConsulta

    def __init__(
        self,
        usuario: UsuarioEntidade | None = None,
        schema: str | None = None,
        somente_leitura: bool = False,
    ):
        self.somente_leitura = somente_leitura

        super().__init__(
            usuario=usuario,
            schema=schema,
        )

    async def __aenter__(self) -> UnidadeDeTrabalho:
        self.commited = False

        # verificar add schema
        self.session = await self.sql_session_factory(
            schema=self.schema, somente_leitura=False
        )
        self.session_leitura = await self.sql_session_factory(
            schema=self.schema,
            somente_leitura=True,
        )

        if not self.somente_leitura and self.domain_repo_class:
            self.domain_repo = self.domain_repo_class(self.session)

        if self.view_repo_class:
            self.view_repo = self.view_repo_class(self.session_leitura)

        return await super().__aenter__()

    async def __aexit__(
        self, *args: tuple[type[Exception], Exception, Exception]
    ) -> None:
        # Isso tem que ficar no final, após fechar as sessões
        await super().__aexit__(*args)
