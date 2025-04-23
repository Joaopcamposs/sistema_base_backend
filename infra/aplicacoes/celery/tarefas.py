import asyncio

import sentry_sdk

from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from infra.aplicacoes.celery import celery_app
from libs.ddd.barramento import Evento


def tarefa_celery(*args, **kwargs):
    max_retries = kwargs.pop("max_retries", 1)

    kwargs["bind"] = True
    kwargs["trail"] = True
    retry_backoff = kwargs.pop("retry_backoff", 5)
    retry_backoff_max = kwargs.pop("retry_backoff_max", 700)
    retry_jitter = kwargs.pop("retry_jitter", False)
    return celery_app.task(
        *args,
        autoretry_for=(Exception,),
        retry_kwargs={"max_retries": max_retries},
        max_retries=max_retries,
        retry_backoff=retry_backoff,
        retry_backoff_max=retry_backoff_max,
        retry_jitter=retry_jitter,
        **kwargs,
    )


@tarefa_celery()
def task_tratar_evento_asyncrono(
    self, evento: Evento, usuario: UsuarioEntidade | None = None
):
    from contextos_de_negocio.barramento import bootstrap

    async def executar(barramento, evento) -> None:
        await barramento.handle(evento)

    nome = f"Tratando evento asyncrono [{evento.__class__.__name__}]"

    # todo registrar evento rodando
    contexto = sentry_sdk.start_transaction(
        name="Tratando evento asyncrono",
        op="task",
        description=nome,
        sampled=True,
    )
    with contexto as span:
        span.set_tag("name", nome)
        try:
            # A execução assíncrona começou, super importante alterar a flag do evento
            # para não ser executado de forma assíncrona novamente,
            # caso contrário o celery entrará num loop infinito de tasks
            evento.executar_de_forma_assincrona = False

            bus = bootstrap(usuario=usuario, subir_erros_de_eventos=True)

            # isso deve rodar dentro do asyncio.run devido a estrutura de funcoes async
            asyncio.run(executar(bus, evento))

        except Exception as erro:
            span.set_tag("houve_erro", True)
            span.set_tag("error", str(erro))
            raise erro
