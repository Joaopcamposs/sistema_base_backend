from celery import Celery

from infra.banco_de_dados import obter_uri_do_celery

celery_uri = obter_uri_do_celery()
celery_app = Celery("tasks", broker=celery_uri, backend=celery_uri)
celery_app.conf.update(
    task_serializer="pickle",
    accept_content=["pickle"],
    result_serializer="pickle",
)
