export COMPOSE_NAME=sistema_base_backend

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