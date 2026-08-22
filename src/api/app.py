"""FastAPI application entrypoint."""

from fastapi import FastAPI

from src.api.routes import router


app = FastAPI(
    title="LLM Data Intelligence System",
    version="1.29.0",
    description="Cognitive Intelligence API",
)


app.include_router(
    router,
)
