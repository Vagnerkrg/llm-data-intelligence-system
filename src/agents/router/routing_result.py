from dataclasses import dataclass, field
from typing import List


@dataclass
class RoutingResult:
    """
    Represents the result of a routing decision.
    Supports single and multi-tool routing.
    """

    tools: List[str] = field(
        default_factory=list
    )

    confidence: float = 0.0

    reason: str = ""



    @property
    def tool(self):
        """
        Backward compatibility.

        Existing components expect
        routing_result.tool.
        """

        if not self.tools:
            return None

        return self.tools[0]