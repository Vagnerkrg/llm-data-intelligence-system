from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.error_handlers import (
    generic_exception_handler
)



def test_generic_exception_handler():


    app = FastAPI()



    app.add_exception_handler(

        Exception,

        generic_exception_handler

    )



    @app.get("/test-error")
    def test_error():


        raise Exception(

            "Unexpected error"

        )



    client = TestClient(

        app,

        raise_server_exceptions=False

    )



    response = client.get(

        "/test-error"

    )



    assert response.status_code == 500



    assert response.json() == {

        "error":

            "internal_error",

        "message":

            "Unable to process request"

    }