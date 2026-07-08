from fastapi import FastAPI

from src.api.routes import router



app = FastAPI(

    title="LLM Data Intelligence System",

    version="1.0.0"

)



app.include_router(
    router
)



@app.get("/")
def health_check():

    return {

        "status": "online",

        "service":
            "LLM Data Intelligence System"

    }