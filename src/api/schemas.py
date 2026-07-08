from typing import Any

from pydantic import BaseModel, Field



class QuestionRequest(BaseModel):
    """
    Incoming user question.
    """

    question: str



class AnswerResponse(BaseModel):
    """
    Standard API response.
    """

    answer: str

    source: str | None = None

    confidence: float | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )