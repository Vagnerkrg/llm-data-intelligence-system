"""Learning request contract."""

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class LearningRequest:
    """Request received by learning pipeline."""

    experience: Any
    context: Any = None
    learning_type: str | None = None