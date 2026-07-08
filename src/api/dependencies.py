from functools import lru_cache

from src.application.intelligence_system import (
    IntelligenceSystem
)


@lru_cache
def get_intelligence_system():
    """
    Returns a singleton instance of
    the Intelligence System.
    """

    return IntelligenceSystem()