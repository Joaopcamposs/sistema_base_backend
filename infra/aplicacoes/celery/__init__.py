from celery import Celery
from barramento_de_mensagens.aplicacoes.celery import configurar_celery_app

from infra.banco_de_dados import obter_uri_do_celery

celery_uri = obter_uri_do_celery()
celery_app = Celery(
    "tarefas",
    broker=celery_uri,
    backend=celery_uri,
    include=[
        "infra.aplicacoes.celery.tarefas",  # <-- seu módulo de tarefas
    ],
)
celery_app.conf.update(
    task_serializer="pickle",
    accept_content=["pickle"],
    result_serializer="pickle",
)
configurar_celery_app(celery_app)
