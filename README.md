# Sistema Base Backend

Sistema base de backend para criar sistemas de gestão de negócios (dentistas, advogados, médicos, etc.). 
A ideia é ter uma base sólida de gerenciamento de processos principais que pode ser adaptada para diferentes domínios.

## Principais Tecnologias

| Tecnologia | Uso |
|------------|-----|
| Python 3.11+ | Linguagem principal |
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web assíncrono |
| SQLAlchemy 2.0 | ORM com suporte async |
| PostgreSQL | Banco de dados relacional |
| Celery | Processamento assíncrono de tarefas |
| Redis | Broker para Celery |
| Docker | Containerização |
| pytest | Testes automatizados |

## Arquitetura

O sistema é baseado em **arquitetura hexagonal**, onde as regras de negócio estão isoladas da infraestrutura.

### Princípios e Padrões

- **SOLID**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **DDD** (Domain Driven Design): Entidades de negócio separadas em contextos delimitados
- **EDD** (Event Driven Design): Comandos e Eventos para comunicação entre componentes
- **Repository Pattern**: Abstração do acesso ao banco de dados
- **Unit of Work**: Gerenciamento de transações e eventos
- **Message Bus**: Roteamento de comandos e eventos para handlers

### Barramento de Mensagens

O sistema utiliza um barramento de mensagens desacoplado que suporta:

- **Comandos**: Ações que modificam estado (ex: `CadastrarUsuario`)
- **Eventos**: Notificações de mudanças de estado (ex: `UsuarioCriado`)
- **Execução Assíncrona**: Eventos podem ser processados via Celery

```python
# Exemplo de uso do barramento
from contextos_de_negocio.barramento.bootstrap import bootstrap

bus = bootstrap(usuario=usuario_logado)
resultado = await bus.handle(CadastrarUsuario(nome="João", email="joao@exemplo.com", ...))
```

### Executor Assíncrono

O barramento suporta execução assíncrona de eventos através do padrão Strategy:

```python
# Para testes - usa executor nulo (não executa de fato)
from libs.barramento_de_mensagens.base.executor_assincrono import ExecutorAssincronoNulo
bus = bootstrap(executor_assincrono=ExecutorAssincronoNulo())

# Para produção - usa Celery (padrão)
from infra.aplicacoes.celery.executor_celery import executor_celery_padrao
bus = bootstrap(executor_assincrono=executor_celery_padrao)
```

### Referências

- [SOLID e DDD no Python](https://medium.com/@habbema/solid-e-ddd-no-python-4cd6ce65f8ba)
- [Domain-Driven Design (Livro)](https://www.amazon.com.br/Domain-Driven-Design-Atacando-Complexidades-Software/dp/8550800651)
- [Cosmic Python (EDD)](https://www.cosmicpython.com/book/introduction.html)
- [Refactoring Guru](https://refactoring.guru/)

## Estrutura do Projeto

```
sistema_base_backend/
├── contextos_de_negocio/     # Domínio e regras de negócio
│   ├── adaptadores/          # Repositórios, ORM, visualizadores
│   ├── barramento/           # Bootstrap, handlers, unidade de trabalho
│   ├── dominio/              # Agregados, entidades, comandos, eventos
│   ├── pontos_de_entrada/    # API REST (FastAPI)
│   └── servicos/             # Executores de comandos/eventos
├── infra/                    # Infraestrutura
│   ├── aplicacoes/celery/    # Configuração Celery e executor assíncrono
│   └── banco_de_dados/       # Configuração do banco e schemas
├── libs/                     # Bibliotecas abstratas reutilizáveis
│   ├── barramento_de_mensagens/  # Message bus, UoW, executor assíncrono
│   ├── ddd/                  # Classes base para DDD
│   └── utils/                # Utilitários (tipos, constantes, exceções)
└── tests/                    # Testes automatizados
    ├── unitarios/            # Testes unitários (sem banco)
    └── integracao/           # Testes de integração (com banco)
```

## Como Executar

### Requisitos
- Docker e Docker Compose
- Make (opcional, mas recomendado)
- Python 3.11+ (para desenvolvimento local)

### Execução com Docker

```bash
# Iniciar todos os serviços (API, Celery, Redis, PostgreSQL)
make compose

# Acessar a documentação da API
open http://localhost:8000/docs
```

### Comandos Úteis

```bash
# Iniciar apenas a API
make api

# Iniciar apenas o worker Celery
make celery

# Iniciar apenas o PostgreSQL
make postgres

# Formatar e verificar código
make ruff

# Verificar tipos
make mypy

# Limpar containers Docker
make docker-clean
```

## Testes

O projeto possui testes unitários e de integração.

### Executar Testes

```bash
# Todos os testes (requer docker-compose de testes)
make test

# Apenas testes unitários (não requer banco)
make test-unit

# Apenas testes de integração (requer banco)
make test-integration

# Testes com cobertura
make test-cov
```

### Ambiente de Testes

```bash
# Subir ambiente de testes (PostgreSQL, Redis, Celery)
make test-env

# Derrubar ambiente de testes
make test-env-down
```

### Estrutura dos Testes

- **Testes Unitários** (`tests/unitarios/`): Testam domínio, agregados, comandos, eventos e barramento sem dependências externas
- **Testes de Integração** (`tests/integracao/`): Testam repositórios, serviços e API com banco de dados real

## Configuração

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DB_HOST` | Host do PostgreSQL | `localhost` |
| `DB_PORT` | Porta do PostgreSQL | `5432` |
| `DB_USER` | Usuário do banco | `postgres` |
| `DB_PASSWORD` | Senha do banco | `password` |
| `DB_NAME` | Nome do banco | `postgres` |
| `REDIS_HOST` | Host do Redis | `localhost` |
| `TEST_ENV` | Ambiente de teste | `false` |
| `ENV_CONFIG` | Ambiente (development/alpha/production) | `development` |

### Secrets

Crie um arquivo `secrets.json` na raiz do projeto:

```json
{
  "AES_KEY": "sua-chave-aes-32-bytes",
  "CHAVE_SECRETA": "sua-chave-secreta",
  "SECRET_KEY": "sua-secret-key-jwt",
  "ALGORITHM": "HS256"
}
```

## Licença

Este projeto é privado e de uso interno.
