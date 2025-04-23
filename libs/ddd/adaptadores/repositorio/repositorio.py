from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from libs.ddd.dominio.agregado import Agregado


class RepositorioAbstrato(ABC):
    def __init__(
        self,
        session: AsyncSession | None = None,
    ) -> None:
        if session is not None:
            self.session = session


class RepositorioDominio(RepositorioAbstrato):
    def __init__(self, *args, **kwargs):
        super(RepositorioDominio, self).__init__(*args, **kwargs)
        self.seen: set[Agregado] = set()

    async def adicionar(self, agregado: Agregado) -> None:
        self.seen.add(agregado)
        await self._adicionar(agregado)

    @abstractmethod
    async def _adicionar(self, agregado: Agregado) -> None:
        raise NotImplementedError

    async def remover(self, agregado: Agregado) -> None:
        await self._remover(agregado)

    @abstractmethod
    async def _remover(self, agregado: Agregado) -> None:
        raise NotImplementedError


class RepositorioConsulta(RepositorioAbstrato): ...
