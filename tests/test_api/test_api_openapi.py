"""OpenAPI contract tests."""

from src.api.app import app


def test_openapi_contains_v129_endpoints() -> None:
    """All public V1.29 endpoints must be present."""
    schema = app.openapi()

    paths = schema["paths"]

    expected_paths = {
        "/api/v1/ask",
        "/api/v1/executions/{execution_id}",
        "/api/v1/executions/{execution_id}/trace",
        "/api/v1/executions/{execution_id}/cognitive-state",
        "/api/v1/executions/{execution_id}/memory",
        "/api/v1/executions/{execution_id}/knowledge",
        "/api/v1/executions/{execution_id}/learning",
        "/api/v1/executions/{execution_id}/evolution",
    }

    assert expected_paths.issubset(
        paths.keys(),
    )


def test_openapi_contains_public_schemas() -> None:
    """OpenAPI must expose the public contract schemas."""
    schema = app.openapi()

    schemas = schema["components"]["schemas"]

    expected_schemas = {
        "ExecutionResponse",
        "ExecutionTraceResponse",
        "CognitiveStateResponse",
        "MemoryResponse",
        "KnowledgeResponse",
        "LearningResponse",
        "EvolutionResponse",
        "APIErrorResponse",
        "APIErrorDetail",
    }

    assert expected_schemas.issubset(
        schemas.keys(),
    )


def test_openapi_uses_api_version() -> None:
    """The API must advertise the current version."""
    assert app.version == "1.29.0"
