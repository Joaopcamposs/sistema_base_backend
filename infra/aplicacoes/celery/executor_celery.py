"""
Implementação do executor assíncrono usando Celery.
Esta implementação pode ser facilmente substituída por outra no futuro.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from libs.barramento_de_mensagens.base.executor_assincrono import (
    ExecutorAssincronoAbstrato,
)

if TYPE_CHECKING:
    from libs.barramento_de_mensagens.base.barramento import Evento
    from libs.barramento_de_mensagens.base.entidades import UsuarioBase


class ExecutorCelery(ExecutorAssincronoAbstrato):
    """
    Implementação do executor assíncrono usando Celery.
    """

    def executar(
        self,
        evento: "Evento",
        usuario: "UsuarioBase | None" = None,
    ) -> Any:
        """
        Executa um evento de forma assíncrona usando Celery.

        Args:
            evento: O evento a ser executado
            usuario: O usuário que disparou o evento

        Returns:
            AsyncResult do Celery
        """
        from infra.aplicacoes.celery.tarefas import task_tratar_evento_asyncrono

        tarefa = task_tratar_evento_asyncrono.si(
            evento=evento,
            usuario=usuario,
        )

        config = self.configurar_tarefa(evento)

        if config.get("countdown"):
            tarefa = tarefa.set(countdown=config["countdown"])

        if config.get("queue"):
            tarefa = tarefa.set(queue=config["queue"])

            if config.get("priority"):
                tarefa = tarefa.set(priority=config["priority"])

        return tarefa.apply_async()


# Instância singleton para uso no barramento
executor_celery_padrao = ExecutorCelery()
