from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from fastapi import FastAPI

from contextos_de_negocio.pontos_de_entrada.api_publica.recursos_cliente import (
    router_cliente,
)
from contextos_de_negocio.pontos_de_entrada.api_publica.recursos_empresa import (
    router_empresa,
)
from contextos_de_negocio.pontos_de_entrada.api_publica.recursos_seguranca import (
    router_seguranca,
)
from contextos_de_negocio.pontos_de_entrada.api_publica.recursos_servico import (
    router_servico,
)
from contextos_de_negocio.pontos_de_entrada.api_publica.recursos_teste import router_teste
from contextos_de_negocio.pontos_de_entrada.api_publica.recursos_usuario import (
    router_usuario,
)
from contextos_de_negocio.pontos_de_entrada.api_publica.registro_de_servico import (
    router_registro_de_servico,
)
from contextos_de_negocio.pontos_de_entrada.api_publica.sessao_de_servicos import (
    router_sessao_de_servicos,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    from infra.banco_de_dados.inicializadores import criar_primeira_empresa_e_usuario
    from barramento_de_mensagens.aplicacoes.celery import configurar_celery_app
    from infra.aplicacoes.celery import celery_app

    await criar_primeira_empresa_e_usuario()
    configurar_celery_app(celery_app)
    yield


app = FastAPI(
    title="API Sistema Base Backend",
    description="APIs REST",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


@app.get("/")
async def test() -> dict[str, str]:
    return {"message": "API está no ar!"}


app.include_router(router_seguranca)
app.include_router(router_teste)
app.include_router(router_empresa)
app.include_router(router_usuario)
app.include_router(router_cliente)
app.include_router(router_servico)
app.include_router(router_sessao_de_servicos)
app.include_router(router_registro_de_servico)
