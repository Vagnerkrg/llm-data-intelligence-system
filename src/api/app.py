"""FastAPI application entrypoint."""

from fastapi import FastAPI

from src.api.routes import (
    router,
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="LLM Data Intelligence System API",
        version="1.29.0",
        description=("Public API contract for the LLM Data Intelligence System."),
    )

    application.include_router(
        router,
    )

    return application


app = create_app()
