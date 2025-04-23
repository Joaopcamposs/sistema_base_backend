import functools
import inspect
from typing import Any

from libs.ddd.barramento import Comando, Evento, BarramentoDeMensagens, logger
from libs.ddd.unidade_de_trabalho import UnidadeDeTrabalhoAbstrata


def bootstrap_base(
    uow: UnidadeDeTrabalhoAbstrata,
    command_handlers: dict[type[Comando], callable],
    event_handlers: dict[Evento, list[callable]],
    subir_erros_de_eventos: bool = False,
    erros_de_eventos_para_subir: list[type[Exception]] | None = None,
    permitir_execucoes_assincronas: bool = True,
) -> BarramentoDeMensagens:
    dependencies = {"uow": uow}

    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies) for handler in event_handlers
        ]
        for event_type, event_handlers in event_handlers.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in command_handlers.items()
    }

    return BarramentoDeMensagens(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
        subir_erros_de_eventos=subir_erros_de_eventos,
        erros_de_eventos_para_subir=erros_de_eventos_para_subir,
        permitir_execucoes_assincronas=permitir_execucoes_assincronas,
    )


def inject_dependencies(handler: callable, dependencies: dict) -> callable:
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }

    if inspect.iscoroutinefunction(handler):

        @functools.wraps(handler)
        async def async_wrapper(message: Comando | Evento) -> Any:
            try:
                return await handler(message, **deps)
            except Exception as erro:
                logger.error(f"Error handling async event {message}. Error: {erro}")
            finally:
                logger.info(f"Handling async event {message} finished")

        return async_wrapper

    @functools.wraps(handler)
    def sync_wrapper(message: Comando | Evento) -> Any:
        try:
            return handler(message, **deps)
        except Exception as erro:
            logger.error(f"Error handling event {message}. Error: {erro}")
        finally:
            logger.info(f"Handling event {message} finished")

    return sync_wrapper
