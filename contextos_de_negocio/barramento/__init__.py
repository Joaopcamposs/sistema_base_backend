from typing import Callable

from barramento_de_mensagens.base.barramento import Evento, Comando, BarramentoDeMensagens
from barramento_de_mensagens.base.unidade_de_trabalho import UnidadeDeTrabalhoAbstrata
from barramento_de_mensagens.bootstrap import bootstrap_base

from contextos_de_negocio.barramento.manipuladores import COMMAND_HANDLERS, EVENT_HANDLERS
from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho


def bootstrap(
    uow: UnidadeDeTrabalhoAbstrata | None = None,
    event_handlers: dict[type[Evento], list[Callable]] | None = None,
    command_handlers: dict[type[Comando], Callable] | None = None,
    usuario: UsuarioEntidade | None = None,
    schema: str | None = None,
    subir_erros_de_eventos: bool = False,
    permitir_execucoes_assincronas: bool = True,
    somente_leitura: bool = False,
    criar_schema: bool = False,
) -> BarramentoDeMensagens:
    if uow is None:
        uow = UnidadeDeTrabalho(
            usuario=usuario,
            schema=schema,
            somente_leitura=somente_leitura,
            criar_schema=criar_schema,
        )

    command_handlers = command_handlers or COMMAND_HANDLERS
    event_handlers = event_handlers or EVENT_HANDLERS

    return bootstrap_base(
        uow=uow,
        command_handlers=command_handlers,
        event_handlers=event_handlers,
        subir_erros_de_eventos=subir_erros_de_eventos,
        permitir_execucoes_assincronas=permitir_execucoes_assincronas,
    )
