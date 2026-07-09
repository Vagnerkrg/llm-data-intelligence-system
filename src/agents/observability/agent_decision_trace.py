from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class AgentDecisionTrace:
    """
    Represents a complete trace of an agent decision.

    Stores the reasoning path and execution information
    generated during an agent interaction.
    """


    question: str

    selected_tool: str | None

    confidence: float

    reason: str

    execution_time: float

    success: bool

    result: Any

    timestamp: datetime