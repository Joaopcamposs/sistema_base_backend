export COMPOSE_NAME=sistema_base_backend

test-env:
	docker-compose -f infra/docker-compose-tests.yml rm && docker-compose -f infra/docker-compose-tests.yml -p $(COMPOSE_NAME)_teste up


docker-clean:
	docker system prune -f

compose:
	docker-compose -f docker-compose.yml --env-file .env -p $(COMPOSE_NAME) up --build -d

api:
	docker-compose -f docker-compose.yml --env-file .env -p $(COMPOSE_NAME) up --build -d api

celery:
	docker-compose -f docker-compose.yml --env-file .env -p $(COMPOSE_NAME) up --build -d celery_worker

postgres:
	docker-compose -f docker-compose.yml --env-file .env -p $(COMPOSE_NAME) up --build -d postgres

ruff:
	ruff format . && ruff check . --fix

mypy:
	mypy .

poetry-install:
	poetry lock && poetry install

poetry-activate:
	poetry env activate

instalar-local:
	poetry remove barramento-de-mensagens && \
	poetry add libs/barramento_de_mensagens-0.1.3-py3-none-any.whl