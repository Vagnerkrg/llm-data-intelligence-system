"""Backward compatibility tests for legacy API contracts."""

from fastapi.testclient import TestClient

from src.api.app import app
from src.api.dependencies import get_intelligence_system


class FakeIntelligenceSystem:
    """Fake legacy intelligence runtime."""

    def ask(
        self,
        question: str,
    ):
        """Return a deterministic fake response."""
        return type(
            "LegacyResponse",
            (),
            {
                "answer": "mock answer",
                "source": "test",
                "confidence": 1.0,
                "metadata": {
                    "question": question,
                },
            },
        )()


app.dependency_overrides[get_intelligence_system] = lambda: FakeIntelligenceSystem()


client = TestClient(app)


def test_legacy_ask_route_remains_registered() -> None:
    """Legacy /ask route must remain available."""

    schema = client.app.openapi()

    assert "/ask" in schema["paths"]


def test_legacy_ask_contract_accepts_question_field() -> None:
    """Legacy /ask endpoint must preserve old request contract."""

    response = client.post(
        "/ask",
        json={
            "question": "legacy compatibility test",
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert "answer" in payload
    assert "source" in payload
    assert "confidence" in payload
    assert "metadata" in payload


def test_legacy_ask_rejects_missing_question() -> None:
    """Legacy endpoint must validate required fields."""

    response = client.post(
        "/ask",
        json={},
    )

    assert response.status_code == 422


def test_legacy_ask_response_is_serializable() -> None:
    """Legacy response must remain JSON compatible."""

    response = client.post(
        "/ask",
        json={
            "question": "serialization test",
        },
    )

    payload = response.json()

    assert isinstance(
        payload,
        dict,
    )


def test_legacy_ask_keeps_api_version() -> None:
    """Legacy route must not break current API version."""

    assert client.app.version == "1.29.0"
