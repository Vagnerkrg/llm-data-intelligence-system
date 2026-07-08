from src.api.dependencies import (
    get_intelligence_system
)


def test_singleton():

    first = get_intelligence_system()

    second = get_intelligence_system()

    assert first is second