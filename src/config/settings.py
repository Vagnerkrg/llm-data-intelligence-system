"""
Application settings.

Loads configuration values from
environment variables.
"""


from pydantic_settings import BaseSettings
from pydantic import ConfigDict


from src.config.constants import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_ENVIRONMENT
)



class Settings(BaseSettings):
    """
    Global application settings.
    """


    app_name: str = APP_NAME


    version: str = APP_VERSION


    environment: str = DEFAULT_ENVIRONMENT


    debug: bool = True


    groq_api_key: str | None = None



    model_config = ConfigDict(

        env_file=".env",

        extra="ignore"

    )



settings = Settings()