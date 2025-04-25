from contextos_de_negocio.barramento.manipuladores import COMMAND_HANDLERS, EVENT_HANDLERS
from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocio.unidade_de_trabalho import UnidadeDeTrabalho
from libs.ddd.barramento import Evento, Comando
from libs.ddd.bootstrap import bootstrap_base
from libs.ddd.unidade_de_trabalho import UnidadeDeTrabalhoAbstrata


def bootstrap(
    uow: UnidadeDeTrabalhoAbstrata | None = None,
    event_handlers: dict[type[Evento], list[callable]] | None = None,
    command_handlers: dict[type[Comando], callable] | None = None,
    usuario: UsuarioEntidade | None = None,
    schema: str | None = None,
    subir_erros_de_eventos: bool = False,
    erros_de_eventos_para_subir: list[type[Exception]] | None = None,
    permitir_execucoes_assincronas: bool = True,
    somente_leitura: bool = False,
    eh_criacao_de_nova_empresa: bool = False,
):
    if uow is None:
        uow = UnidadeDeTrabalho(
            usuario=usuario,
            schema=schema,
            somente_leitura=somente_leitura,
            eh_criacao_de_nova_empresa=eh_criacao_de_nova_empresa,
        )

    command_handlers = command_handlers or COMMAND_HANDLERS
    event_handlers = event_handlers or EVENT_HANDLERS

    return bootstrap_base(
        uow=uow,
        command_handlers=command_handlers,
        event_handlers=event_handlers,
        subir_erros_de_eventos=subir_erros_de_eventos,
        erros_de_eventos_para_subir=erros_de_eventos_para_subir,
        permitir_execucoes_assincronas=permitir_execucoes_assincronas,
    )
