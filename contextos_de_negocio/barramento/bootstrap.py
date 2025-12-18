from typing import Callable, TYPE_CHECKING

from libs.barramento_de_mensagens.base.barramento import BarramentoDeMensagens
from libs.barramento_de_mensagens.bootstrap import bootstrap_base
from libs.barramento_de_mensagens.manipuladores import (
    ManipuladoresDeEventos,
    ManipuladoresDeComandos,
)
from libs.barramento_de_mensagens.unidade_de_trabalho import UnidadeDeTrabalhoBase
from sqlalchemy.orm import DeclarativeBase

from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from infra.banco_de_dados import DEFAULT_SQL_SESSION_FACTORY, get_sql_engine
from libs.ddd.adaptadores.orm.declarativo import Base

if TYPE_CHECKING:
    from libs.barramento_de_mensagens.base.executor_assincrono import (
        ExecutorAssincronoProtocol,
    )


def bootstrap(
    session_factory: Callable = DEFAULT_SQL_SESSION_FACTORY,
    engine_factory: Callable = get_sql_engine,
    base: type[DeclarativeBase] = Base,
    event_handlers: ManipuladoresDeEventos | None = None,
    command_handlers: ManipuladoresDeComandos | None = None,
    uow: UnidadeDeTrabalhoBase | None = None,
    usuario: UsuarioEntidade | None = None,
    schema: str | None = None,
    subir_erros_de_eventos: bool = False,
    permitir_execucoes_assincronas: bool = True,
    somente_leitura: bool = False,
    criar_schema: bool = False,
    executor_assincrono: "ExecutorAssincronoProtocol | None" = None,
) -> BarramentoDeMensagens:
    # importe seus manipuladores
    from contextos_de_negocio.barramento.manipuladores import (
        COMMAND_HANDLERS,
        EVENT_HANDLERS,
    )
    from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho

    # defina seus manipuladores
    command_handlers = command_handlers or COMMAND_HANDLERS
    event_handlers = event_handlers or EVENT_HANDLERS

    if uow is None:
        uow = UnidadeDeTrabalho(
            usuario=usuario,
            schema=schema,
            somente_leitura=somente_leitura,
            criar_schema=criar_schema,
        )

    # Configura executor assíncrono padrão (Celery) se não fornecido e assíncrono habilitado
    if executor_assincrono is None and permitir_execucoes_assincronas:
        from infra.aplicacoes.celery.executor_celery import executor_celery_padrao

        executor_assincrono = executor_celery_padrao

    return bootstrap_base(
        uow=uow,
        session_factory=session_factory,
        engine_factory=engine_factory,
        base=base,
        event_handlers=event_handlers,
        command_handlers=command_handlers,
        usuario=usuario,
        schema=schema,
        subir_erros_de_eventos=subir_erros_de_eventos,
        permitir_execucoes_assincronas=permitir_execucoes_assincronas,
        somente_leitura=somente_leitura,
        criar_schema=criar_schema,
        executor_assincrono=executor_assincrono,
    )
