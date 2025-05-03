FROM python:3.11.9-slim

# Cria diretório da app
WORKDIR /sistema_base_backend

# Instalações básicas
RUN apt-get update && apt-get install -y curl build-essential

# Instala o Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Define o Poetry para criar o virtualenv dentro do projeto
RUN poetry config virtualenvs.in-project true

# Copia a aplicação
COPY . .

# Instala dependências
RUN poetry lock && poetry install --no-root

# Adiciona o .venv/bin ao PATH do container
ENV PATH="/sistema_base_backend/.venv/bin:$PATH"

# Comando padrão
CMD ["uvicorn", "contextos_de_negocio.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "uvicorn_logging_config.json"]
