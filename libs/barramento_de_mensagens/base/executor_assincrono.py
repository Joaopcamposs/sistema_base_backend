"""
Módulo que define o protocolo para execução assíncrona de eventos.

Este módulo implementa o padrão Strategy para execução assíncrona de eventos,
permitindo desacoplar o barramento de mensagens de implementações específicas
como Celery, RabbitMQ, ou qualquer outro sistema de filas.

Exemplo de uso:
    ```python
    from libs.barramento_de_mensagens.base.executor_assincrono import (
        ExecutorAssincronoNulo,
        ExecutorAssincronoProtocol,
    )

    # Para testes - usa executor nulo que apenas registra eventos
    executor = ExecutorAssincronoNulo()

    # Para produção - use a implementação Celery
    from infra.aplicacoes.celery.executor_celery import ExecutorCelery
    executor = ExecutorCelery()

    # Passar o executor ao bootstrap
    bus = bootstrap(executor_assincrono=executor)
    ```

Classes:
    ExecutorAssincronoProtocol: Protocolo (interface) para executores.
    ExecutorAssincronoAbstrato: Classe base abstrata com métodos comuns.
    ExecutorAssincronoNulo: Implementação para testes (não executa de fato).
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

    Implementações concretas podem usar Celery, RabbitMQ, Redis Queue,
    ou qualquer outro sistema de filas/mensageria.

    Este protocolo usa `@runtime_checkable` para permitir verificação
    de tipo em runtime com `isinstance()`.

    Example:
        ```python
        def meu_executor(executor: ExecutorAssincronoProtocol):
            if isinstance(executor, ExecutorAssincronoProtocol):
                executor.executar(evento)
        ```
    """

    def executar(
        self,
        evento: "Evento",
        usuario: "UsuarioBase | None" = None,
    ) -> Any:
        """
        Executa um evento de forma assíncrona.

        Args:
            evento: O evento a ser executado.
            usuario: O usuário que disparou o evento (para contexto).

        Returns:
            Resultado da execução (ex: task_id do Celery, message_id do RabbitMQ).
        """
        ...


class ExecutorAssincronoAbstrato(ABC):
    """
    Classe base abstrata para executores assíncronos.

    Fornece implementação da funcao `configurar_tarefa` que extrai
    configurações do evento (delay, fila, prioridade) para uso
    nas implementações concretas.

    Attributes:
        Nenhum atributo de instância definido na classe base.

    Methods:
        executar: funcao abstrata a ser implementada.
        configurar_tarefa: Extrai configurações do evento.
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
            evento: O evento a ser executado.
            usuario: O usuário que disparou o evento.

        Returns:
            Resultado específico da implementação.

        Raises:
            NotImplementedError: Se não implementado pela subclasse.
        """
        raise NotImplementedError

    def configurar_tarefa(self, evento: "Evento") -> dict[str, Any]:
        """
        Extrai configurações de execução do evento.

        Lê os atributos do evento relacionados à execução assíncrona
        e retorna um dicionário com as configurações para a tarefa.

        Args:
            evento: Evento com configurações de execução.

        Returns:
            Dicionário com chaves opcionais:
                - countdown: Delay em segundos antes de executar.
                - queue: Nome da fila de destino.
                - priority: Prioridade na fila (se suportado).

        Example:
            ```python
            evento = MeuEvento(
                tempo_de_atraso_para_execucao_assincrona=30,
                fila_de_execucao_assincrona="alta_prioridade",
                prioridade_de_execucao_assincrona=10,
            )
            config = executor.configurar_tarefa(evento)
            # config = {"countdown": 30, "queue": "alta_prioridade", "priority": 10}
            ```
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
    Implementação nula do executor assíncrono (Null Object Pattern).

    Esta implementação NÃO executa eventos de fato, apenas os registra
    em uma lista interna. É útil para:

    - Testes unitários: verificar quais eventos foram disparados.
    - Desenvolvimento local: evitar dependência de Celery/Redis.
    - Debug: inspecionar eventos sem efeitos colaterais.

    Attributes:
        eventos_executados: Lista de tuplas (evento, usuario) registradas.

    Example:
        ```python
        executor = ExecutorAssincronoNulo()

        # Simula execução
        executor.executar(MeuEvento(dados="teste"), usuario=meu_usuario)

        # Verifica o que foi "executado"
        assert len(executor.eventos_executados) == 1
        evento, usuario = executor.eventos_executados[0]
        assert evento.dados == "teste"

        # Limpa para próximo teste
        executor.limpar()
        ```
    """

    def __init__(self) -> None:
        """Inicializa o executor com lista vazia de eventos."""
        self.eventos_executados: list[tuple["Evento", "UsuarioBase | None"]] = []

    def executar(
        self,
        evento: "Evento",
        usuario: "UsuarioBase | None" = None,
    ) -> None:
        """
        Registra o evento sem executá-lo de fato.

        Args:
            evento: O evento a ser registrado.
            usuario: O usuário associado ao evento.
        """
        self.eventos_executados.append((evento, usuario))

    def limpar(self) -> None:
        """Limpa a lista de eventos executados."""
        self.eventos_executados.clear()
