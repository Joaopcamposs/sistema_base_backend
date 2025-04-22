# noinspection PyUnresolvedReferences
from infra.aplicacoes.celery import celery_app

# Só serve para rodar com: celery -A app.worker worker --loglevel=info
