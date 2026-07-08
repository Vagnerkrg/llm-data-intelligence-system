"""
Health check API routes.

Provides service availability
information for monitoring systems.
"""


from fastapi import APIRouter

from src.config import settings
from src.config.constants import HEALTH_ENDPOINT



router = APIRouter()



@router.get(
    HEALTH_ENDPOINT
)
def health_check():

    return {

        "status": "healthy",

        "app": settings.app_name,

        "version": settings.version,

        "environment": settings.environment

    }