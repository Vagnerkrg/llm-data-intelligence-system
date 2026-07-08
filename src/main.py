from fastapi import FastAPI

from src.api.routes import router
from src.config.settings import settings



app = FastAPI(

    title=settings.app_name,

    version=settings.version

)



app.include_router(

    router

)



@app.get("/")
def health_check():


    return {

        "status":

            "online",

        "service":

            settings.app_name,

        "version":

            settings.version

    }