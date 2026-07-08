from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.health import router



def test_health_endpoint():


    app = FastAPI()


    app.include_router(
        router
    )


    client = TestClient(
        app
    )


    response = client.get(
        "/health"
    )


    assert response.status_code == 200


    assert response.json() == {

        "status": "healthy",

        "app": "LLM Data Intelligence System",

        "version": "1.5.0",

        "environment": "development"

    }