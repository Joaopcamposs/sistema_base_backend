from celery import Celery
from barramento_de_mensagens.aplicacoes.celery import configurar_celery_app

from infra.banco_de_dados import obter_uri_do_celery

celery_uri = obter_uri_do_celery()
celery_app = Celery(
    "tarefas",
    broker=celery_uri,
    backend=celery_uri,
)
celery_app.conf.update(
    task_serializer="pickle",
    accept_content=["pickle"],
    result_serializer="pickle",
)

# Configura o celery app ANTES de importar qualquer tarefa
configurar_celery_app(celery_app)

# Agora sim você importa as tarefas
import infra.aplicacoes.celery.tarefas  # noqa: E402

# Depois se quiser, registra manualmente as tarefas no celery (não precisa de 'include')
celery_app.autodiscover_tasks(["infra.aplicacoes.celery"])

# E adiciona essa linha para tornar o app visível para o Celery
__all__ = ("celery_app",)
