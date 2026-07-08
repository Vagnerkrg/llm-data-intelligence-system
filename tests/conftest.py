"""
Pytest shared fixtures.

Provides reusable test components
across the test suite.
"""


import pytest


from src.core.interfaces.response import (
    IntelligenceResponse
)



@pytest.fixture
def sample_intelligence_response():

    return IntelligenceResponse(

        answer="Test response",

        source="test",

        confidence=1.0,

        metadata={

            "test": True

        }

    )