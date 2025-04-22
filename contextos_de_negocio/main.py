import sentry_sdk
from fastapi import FastAPI


sentry_sdk.init(
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    enable_tracing=True,
)


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
