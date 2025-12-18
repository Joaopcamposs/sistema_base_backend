"""
Módulo que define a classe abstrata UnidadeDeTrabalhoAbstrata.

A Unidade de Trabalho (Unit of Work) é um padrão que mantém uma lista de objetos
afetados por uma transação de negócio e coordena a escrita de mudanças.
"""

from __future__ import annotations

from abc import ABC
from typing import Callable, Any, Generator, TYPE_CHECKING
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from libs.barramento_de_mensagens.base.entidades import (
    RepositorioDominioBase,
    RepositorioConsultaBase,
    UsuarioBase,
)

if TYPE_CHECKING:
    from libs.barramento_de_mensagens.base.barramento import Evento
    from libs.barramento_de_mensagens.dominio import DominioBase


class UnidadeDeTrabalhoSchemaComProblema(Exception):
    """Exceção lançada quando há problema com o schema da unidade de trabalho."""

    pass


class TentandoAbrirUOWContextoJaAberto(Exception):
    """Exceção lançada ao tentar abrir um contexto de UoW já aberto."""

    pass


class UnidadeDeTrabalhoAbstrata(ABC):
    """
    Classe abstrata que define o contrato para Unidades de Trabalho.

    Attributes:
        domain_repo: Repositório de domínio para operações de escrita.
        view_repo: Repositório de consulta para operações de leitura.
        session: Sessão do SQLAlchemy para escrita.
        session_leitura: Sessão do SQLAlchemy para leitura.
        usuario: Usuário que está executando as operações.
        schema: Schema do banco de dados (geralmente o ID da empresa).
    """

    domain_repo: RepositorioDominioBase
    view_repo: RepositorioConsultaBase
    domain_repo_class: type[RepositorioDominioBase]
    view_repo_class: type[RepositorioConsultaBase]
    commited: bool
    session: AsyncSession
    session_leitura: AsyncSession
    usuario: UsuarioBase | None
    schema: str | None = None
    criar_schema: bool = False
    eventos_fora_de_agregado: list["Evento"]

    def __init__(
        self,
        session_factory: Callable[..., AsyncSession],
        usuario: UsuarioBase | None = None,
        schema: str | None = None,
        criar_schema: bool = False,
    ) -> None:
        """
        Inicializa a Unidade de Trabalho.

        Args:
            session_factory: Factory para criar sessões do SQLAlchemy.
            usuario: Usuário que está executando as operações.
            schema: Schema do banco de dados (opcional, usa empresa do usuário).
            criar_schema: Se True, cria o schema se não existir.

        Raises:
            UnidadeDeTrabalhoSchemaComProblema: Se o usuário não pertence ao schema
                ou se nenhum usuário foi fornecido.
        """
        self.sql_session_factory = session_factory
        self.usuario = usuario
        self.criar_schema = criar_schema

        if (
            all([schema, usuario, str(usuario.empresa) != str(schema)])  # type: ignore
            and not criar_schema
        ):
            raise UnidadeDeTrabalhoSchemaComProblema(
                "O usuário não pertence a esse schema."
            )

        if not self.usuario:
            raise UnidadeDeTrabalhoSchemaComProblema(
                "Toda unidade de trabalho deve ter um usuario."
            )

        self.schema = schema or str(self.usuario.empresa)
        self._contexto_ativo = False
        self.eventos_fora_de_agregado = []

    def __call__(
        self,
        repo_por_dominio: "DominioBase | None" = None,
    ) -> UnidadeDeTrabalhoAbstrata:
        """
        Configura os repositórios baseado no domínio.

        Args:
            repo_por_dominio: Enum do domínio contendo classes de repositório.

        Returns:
            A própria instância para permitir encadeamento.
        """
        if repo_por_dominio:
            self.domain_repo_class = repo_por_dominio.value[0]
            self.view_repo_class = repo_por_dominio.value[1]

        return self

    async def __aenter__(self) -> UnidadeDeTrabalhoAbstrata:
        """Entra no contexto da unidade de trabalho."""
        self.commited = False

        if self._contexto_ativo:
            raise TentandoAbrirUOWContextoJaAberto()

        self._contexto_ativo = True
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Sai do contexto da unidade de trabalho."""
        self._contexto_ativo = False

        if not self.commited:
            await self.rollback()

        if hasattr(self, "session"):
            await self.session.close()

    def adicionar_evento_fora_de_agregado(self, evento: "Evento") -> None:
        """
        Adiciona um evento que não pertence a nenhum agregado.

        Args:
            evento: Evento a ser adicionado à fila de processamento.
        """
        self.eventos_fora_de_agregado.append(evento)

    def collect_new_events(self) -> Generator["Evento", None, None]:
        """
        Coleta todos os novos eventos gerados pelos agregados e fora deles.

        Yields:
            Eventos pendentes de processamento.
        """
        if hasattr(self, "domain_repo") and self.domain_repo:
            for agregado in getattr(self.domain_repo, "seen", set()):
                while getattr(agregado, "eventos", []):
                    yield agregado.eventos.pop(0)

        while self.eventos_fora_de_agregado:
            yield self.eventos_fora_de_agregado.pop(0)

    async def commit(self) -> None:
        """Confirma todas as alterações na sessão."""
        await self.session.commit()
        self.commited = True

    async def rollback(self) -> None:
        """Desfaz todas as alterações pendentes."""
        if hasattr(self, "session"):
            await self.session.close()

    @property
    def empresa(self) -> UUID:
        """Retorna o ID da empresa do usuário."""
        if self.usuario and self.usuario.empresa:
            return self.usuario.empresa
        raise ValueError("Id da empresa não foi encontrado")
