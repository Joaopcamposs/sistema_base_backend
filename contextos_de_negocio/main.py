from contextlib import asynccontextmanager

from fastapi import FastAPI

from contextos_de_negocio.pontos_de_entrada.api_publica.recursos_empresa import (
    router_empresa,
)
from contextos_de_negocio.pontos_de_entrada.api_publica.recursos_seguranca import (
    router_seguranca,
)
from contextos_de_negocio.pontos_de_entrada.api_publica.recursos_teste import router_teste
from contextos_de_negocio.pontos_de_entrada.api_publica.recursos_usuario import (
    router_usuario,
)
from infra.banco_de_dados.inicializadores import criar_primeira_empresa_e_usuario


@asynccontextmanager
async def lifespan(app: FastAPI):
    await criar_primeira_empresa_e_usuario()
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
async def test():
    return {"message": "API está no ar!"}


app.include_router(router_seguranca)
app.include_router(router_teste)
app.include_router(router_empresa)
app.include_router(router_usuario)
