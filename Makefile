export COMPOSE_NAME=sistema_base_backend

# ==================== Docker Commands ====================

test-env:
	docker-compose -f infra/docker-compose-tests.yml rm -f && docker-compose -f infra/docker-compose-tests.yml -p $(COMPOSE_NAME)_teste up -d

test-env-down:
	docker-compose -f infra/docker-compose-tests.yml -p $(COMPOSE_NAME)_teste down -v

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

# ==================== Test Commands ====================

test: test-env
	@echo "Aguardando banco de dados ficar pronto..."
	@sleep 5
	TEST_ENV=true pytest tests/ -v --tb=short

test-unit:
	TEST_ENV=true pytest tests/unitarios/ -v --tb=short

test-integration: test-env
	@echo "Aguardando banco de dados ficar pronto..."
	@sleep 5
	TEST_ENV=true pytest tests/integracao/ -v --tb=short

test-cov: test-env
	@echo "Aguardando banco de dados ficar pronto..."
	@sleep 5
	TEST_ENV=true pytest tests/ -v --cov=contextos_de_negocio --cov=libs --cov-report=html --cov-report=term

# ==================== Code Quality ====================

ruff:
	ruff format . && ruff check . --fix

mypy:
	mypy .

lint: ruff mypy