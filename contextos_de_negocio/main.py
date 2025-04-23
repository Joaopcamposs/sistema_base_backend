from fastapi import FastAPI

from contextos_de_negocio.pontos_de_entrada.api_publica.recursos_teste import router_teste

app = FastAPI(
    title="API Sistema Base Backend",
    description="APIs REST",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.get("/")
async def root():
    return {"message": "API está no ar!"}


app.include_router(router_teste)
