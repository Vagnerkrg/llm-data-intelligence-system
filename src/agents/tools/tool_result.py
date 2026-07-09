from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ToolResult:
    """
    Standard result object returned by agent tools.

    Provides a consistent contract between:

    Tool
        |
        v
    AgentController
        |
        v
    Decision / Response Layers
    """

    tool: str

    success: bool

    data: Dict[str, Any]

    metadata: Dict[str, Any]