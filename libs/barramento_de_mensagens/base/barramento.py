"""
Módulo que define o Barramento de Mensagens (Message Bus).

O barramento é responsável por rotear comandos e eventos para seus respectivos
handlers, coordenando a execução e coleta de novos eventos gerados.
"""

from __future__ import annotations

import logging
import os
from abc import ABC
from dataclasses import asdict, dataclass
from typing import Callable, Any, TYPE_CHECKING

import sentry_sdk

from libs.barramento_de_mensagens.base.unidade_de_trabalho import (
    UnidadeDeTrabalhoAbstrata,
)

if TYPE_CHECKING:
    from libs.barramento_de_mensagens.base.executor_assincrono import (
        ExecutorAssincronoProtocol,
    )

logger = logging.getLogger(__name__)

# Campos que devem ser censurados em logs
CAMPOS_SENSIVEIS = frozenset({"senha", "password", "token", "pwd", "secret"})


@dataclass
class BaseComandoOuEvento(ABC):
    """Classe base para Comandos e Eventos com censura de campos sensíveis."""

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if "__repr__" in cls.__dict__:
            cls.__repr__ = BaseComandoOuEvento.__repr__
        if "__str__" in cls.__dict__:
            cls.__str__ = BaseComandoOuEvento.__str__
        return super().__new__(cls)

    def __repr__(self) -> str:
        dados = asdict(self)
        for campo in CAMPOS_SENSIVEIS:
            if campo in dados:
                dados[campo] = "***"
        dados_str = ", ".join([f"{k}={v!r}" for k, v in dados.items()])
        return f"{self.__class__.__name__}({dados_str})"

    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class Comando(BaseComandoOuEvento):
    """Classe base para todos os comandos do sistema."""

    pass


@dataclass(kw_only=True)
class Evento(BaseComandoOuEvento):
    """
    Classe base para todos os eventos do sistema.

    Attributes:
        executar_de_forma_assincrona: Se True, o evento será processado de forma assíncrona.
        fila_de_execucao_assincrona: Nome da fila para processamento assíncrono.
        prioridade_de_execucao_assincrona: Prioridade do evento na fila (maior = mais prioritário).
        tempo_de_atraso_para_execucao_assincrona: Delay em segundos antes de processar.
    """

    executar_de_forma_assincrona: bool = False
    fila_de_execucao_assincrona: str | None = None
    prioridade_de_execucao_assincrona: int | None = None
    tempo_de_atraso_para_execucao_assincrona: int | None = None


Mensagem = Comando | Evento


class BarramentoDeMensagens:
    """
    Barramento de Mensagens que roteia comandos e eventos para handlers.

    O barramento processa uma mensagem por vez, coletando novos eventos
    gerados durante o processamento e adicionando-os à fila.

    Attributes:
        uow: Unidade de trabalho para gerenciar transações.
        event_handlers: Mapa de tipos de evento para lista de handlers.
        command_handlers: Mapa de tipos de comando para handler único.
        subir_erros_de_eventos: Se True, propaga exceções de handlers de evento.
        permitir_execucoes_assincronas: Se True, permite execução assíncrona de eventos.
        executor_assincrono: Executor para processar eventos assíncronos.
    """

    def __init__(
        self,
        uow: UnidadeDeTrabalhoAbstrata,
        event_handlers: dict[type[Evento], list[Callable[..., Any]]],
        command_handlers: dict[type[Comando], Callable[..., Any]],
        subir_erros_de_eventos: bool = True,
        permitir_execucoes_assincronas: bool = False,
        executor_assincrono: "ExecutorAssincronoProtocol | None" = None,
    ) -> None:
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.subir_erros_de_eventos = subir_erros_de_eventos
        self.permitir_execucoes_assincronas = permitir_execucoes_assincronas
        self.executor_assincrono = executor_assincrono
        self.queue: list[Mensagem] = []

    async def handle(self, message: Mensagem) -> Any | None:
        """
        Processa uma mensagem (comando ou evento).

        Args:
            message: Comando ou Evento a ser processado.

        Returns:
            Resultado do comando, se a mensagem for um comando.
        """
        self.queue = [message]
        command_result: Any | None = None

        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, Evento):
                await self._handle_event(message)
            elif isinstance(message, Comando):
                command_result = await self._handle_command(message)
            else:
                raise TypeError(f"{message} não é um Evento ou Comando")

        return command_result

    async def _handle_event(self, event: Evento) -> None:
        """Processa um evento, delegando para execução assíncrona se configurado."""
        if self.permitir_execucoes_assincronas and event.executar_de_forma_assincrona:
            await self._handle_async_event(event)
            return

        for handler in self.event_handlers.get(type(event), []):
            try:
                logger.debug(f"Processando evento {event} com handler {handler}")
                await handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception as erro:
                logger.exception(f"Erro ao processar evento {event}")
                self._handle_event_error(erro)

    def _handle_event_error(self, erro: Exception) -> None:
        """Trata erros de processamento de eventos."""
        if self.subir_erros_de_eventos or os.getenv("TEST_ENV") == "true":
            raise erro

        if os.getenv("ENV_CONFIG", "development") in ["alpha", "production"]:
            sentry_sdk.capture_exception(erro)

    async def _handle_async_event(self, event: Evento) -> None:
        """Delega evento para processamento assíncrono."""
        if self.executor_assincrono is None:
            logger.warning(
                f"Evento {event} marcado para execução assíncrona, "
                "mas nenhum executor foi configurado. Executando de forma síncrona."
            )
            event.executar_de_forma_assincrona = False
            await self._handle_event(event)
            return

        self.executor_assincrono.executar(evento=event, usuario=self.uow.usuario)

    async def _handle_command(self, command: Comando) -> Any | None:
        """Processa um comando."""
        logger.debug(f"Processando comando {command}")
        try:
            handler = self.command_handlers[type(command)]
            result = await handler(command)
            self.queue.extend(self.uow.collect_new_events())
            return result
        except Exception:
            logger.exception(f"Erro ao processar comando {command}")
            raise
