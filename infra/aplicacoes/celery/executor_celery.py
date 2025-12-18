"""
Implementação do executor assíncrono usando Celery.

Este módulo fornece a implementação concreta do ExecutorAssincronoProtocol
usando Celery como backend de processamento assíncrono.

O Celery é configurado para usar Redis como broker e backend de resultados
(configuração em `infra/aplicacoes/celery/__init__.py`).

Exemplo de uso:
    ```python
    from infra.aplicacoes.celery.executor_celery import ExecutorCelery, executor_celery_padrao

    # Usar instância singleton (recomendado)
    executor = executor_celery_padrao

    # Ou criar nova instância
    executor = ExecutorCelery()

    # Executar evento assíncrono
    resultado = executor.executar(meu_evento, usuario=meu_usuario)
    print(f"Task ID: {resultado.id}")
    ```

Configuração de Eventos:
    Os eventos podem ser configurados com os seguintes atributos:
    - `executar_de_forma_assincrona`: True para habilitar processamento assíncrono.
    - `tempo_de_atraso_para_execucao_assincrona`: Delay em segundos (countdown).
    - `fila_de_execucao_assincrona`: Nome da fila Celery de destino.
    - `prioridade_de_execucao_assincrona`: Prioridade da tarefa (0-9, maior = mais prioritário).

Filas Disponíveis:
    Por padrão, o Celery usa a fila "celery". Configure filas adicionais
    no worker para processamento diferenciado:
    ```bash
    celery -A infra.aplicacoes.celery worker -Q celery,alta_prioridade,baixa_prioridade
    ```
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from libs.barramento_de_mensagens.base.executor_assincrono import (
    ExecutorAssincronoAbstrato,
)

if TYPE_CHECKING:
    from celery.result import AsyncResult
    from libs.barramento_de_mensagens.base.barramento import Evento
    from libs.barramento_de_mensagens.base.entidades import UsuarioBase


class ExecutorCelery(ExecutorAssincronoAbstrato):
    """
    Implementação do executor assíncrono usando Celery.

    Esta classe encapsula a lógica de envio de eventos para processamento
    assíncrono via Celery. Os eventos são serializados usando pickle e
    enviados para o worker Celery configurado.

    A tarefa `task_tratar_evento_asyncrono` no worker é responsável por:
    1. Deserializar o evento
    2. Criar um novo bootstrap do barramento de mensagens
    3. Processar o evento com seus handlers

    Attributes:
        Nenhum atributo de instância específico.

    Note:
        Esta classe não mantém estado. Múltiplas instâncias ou a instância
        singleton `executor_celery_padrao` podem ser usadas de forma intercambiável.
    """

    def executar(
        self,
        evento: "Evento",
        usuario: "UsuarioBase | None" = None,
    ) -> "AsyncResult":
        """
        Executa um evento de forma assíncrona usando Celery.

        O evento é enviado para a tarefa `task_tratar_evento_asyncrono`
        que será processada pelo worker Celery.

        Args:
            evento: O evento a ser executado. Deve ser serializável com pickle.
            usuario: O usuário que disparou o evento. Usado para contexto
                    no processamento (ex: auditoria, permissões).

        Returns:
            AsyncResult: Objeto do Celery para rastrear o status da tarefa.
                        Use `.id` para obter o task_id, `.get()` para aguardar
                        o resultado (bloqueante), ou `.ready()` para verificar
                        se completou.

        Example:
            ```python
            executor = ExecutorCelery()

            # Evento simples
            resultado = executor.executar(MeuEvento(dados="teste"))
            print(f"Tarefa enviada: {resultado.id}")

            # Evento com delay de 30 segundos
            evento = MeuEvento(
                dados="agendado",
                executar_de_forma_assincrona=True,
                tempo_de_atraso_para_execucao_assincrona=30,
            )
            resultado = executor.executar(evento, usuario=meu_usuario)

            # Verificar status (não bloqueante)
            if resultado.ready():
                print("Tarefa completada!")
            ```
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
"""
Instância singleton do ExecutorCelery.

Use esta instância em vez de criar novas para evitar overhead desnecessário.
O bootstrap de `contextos_de_negocio` usa esta instância por padrão quando
`permitir_execucoes_assincronas=True` e nenhum executor é fornecido.
"""
