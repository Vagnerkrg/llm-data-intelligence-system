from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.routes import router
from src.api.dependencies import get_intelligence_system

from src.core.interfaces.response import IntelligenceResponse



def test_ask_endpoint():

    class FakeSystem:

        def ask(
            self,
            question
        ):

            return IntelligenceResponse(

                answer="Resposta de teste",

                source="test"

            )



    app = FastAPI()

    app.include_router(router)



    app.dependency_overrides[

        get_intelligence_system

    ] = lambda: FakeSystem()



    client = TestClient(app)



    response = client.post(

        "/ask",

        json={

            "question": "Olá"

        }

    )



    assert response.status_code == 200



    assert response.json() == {

        "answer": "Resposta de teste",

        "source": "test",

        "confidence": None,

        "metadata": {}

    }