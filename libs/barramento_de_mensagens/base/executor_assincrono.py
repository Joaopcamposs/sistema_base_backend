"""
Módulo que define o protocolo para execução assíncrona de eventos.
Este protocolo permite desacoplar o barramento de mensagens de implementações
específicas como Celery, permitindo fácil substituição e testes.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from libs.barramento_de_mensagens.base.barramento import Evento
    from libs.barramento_de_mensagens.base.entidades import UsuarioBase


@runtime_checkable
class ExecutorAssincronoProtocol(Protocol):
    """
    Protocolo que define a interface para executores assíncronos.
    Implementações concretas podem usar Celery, RabbitMQ, ou qualquer outro sistema.
    """

    def executar(
        self,
        evento: "Evento",
        usuario: "UsuarioBase | None" = None,
    ) -> Any:
        """
        Executa um evento de forma assíncrona.

        Args:
            evento: O evento a ser executado
            usuario: O usuário que disparou o evento (opcional)

        Returns:
            Qualquer resultado da execução (ex: task id do Celery)
        """
        ...


class ExecutorAssincronoAbstrato(ABC):
    """
    Classe base abstrata para executores assíncronos.
    Fornece uma implementação base que pode ser estendida.
    """

    @abstractmethod
    def executar(
        self,
        evento: "Evento",
        usuario: "UsuarioBase | None" = None,
    ) -> Any:
        """
        Executa um evento de forma assíncrona.

        Args:
            evento: O evento a ser executado
            usuario: O usuário que disparou o evento (opcional)

        Returns:
            Qualquer resultado da execução
        """
        raise NotImplementedError

    def configurar_tarefa(
        self,
        evento: "Evento",
    ) -> dict[str, Any]:
        """
        Configura os parâmetros da tarefa assíncrona baseado no evento.

        Args:
            evento: O evento com configurações de execução

        Returns:
            Dicionário com configurações da tarefa
        """
        config: dict[str, Any] = {}

        if evento.tempo_de_atraso_para_execucao_assincrona:
            config["countdown"] = evento.tempo_de_atraso_para_execucao_assincrona

        if evento.fila_de_execucao_assincrona:
            config["queue"] = evento.fila_de_execucao_assincrona

            if evento.prioridade_de_execucao_assincrona:
                config["priority"] = evento.prioridade_de_execucao_assincrona

        return config


class ExecutorAssincronoNulo(ExecutorAssincronoAbstrato):
    """
    Implementação nula do executor assíncrono.
    Útil para testes ou quando não se deseja execução assíncrona real.
    """

    def __init__(self) -> None:
        self.eventos_executados: list[tuple["Evento", "UsuarioBase | None"]] = []

    def executar(
        self,
        evento: "Evento",
        usuario: "UsuarioBase | None" = None,
    ) -> None:
        """
        Registra o evento sem executá-lo de fato.
        Útil para testes e verificação.
        """
        self.eventos_executados.append((evento, usuario))

    def limpar(self) -> None:
        """Limpa a lista de eventos executados."""
        self.eventos_executados.clear()
