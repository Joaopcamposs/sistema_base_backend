export COMPOSE_NAME=sistema_base_backend

docker-clean:
	docker system prune -f

compose:
	docker-compose -f docker-compose.yml --env-file .env -p $(COMPOSE_NAME) up --build -d

format:
	ruff format .

ruff:
	ruff format . && ruff check . --fix

mypy:
	mypy .

restore:
	@echo Executando restore.bat...
	cd infra/banco_de_dados && @cmd /c backup_prod_local.bat

poetry-install:
	poetry lock && poetry install

poetry-activate:
	poetry env activate