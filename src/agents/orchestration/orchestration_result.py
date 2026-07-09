from dataclasses import dataclass, field
from typing import Any, Dict, Optional



@dataclass
class OrchestrationResult:
    """
    Represents the final result
    produced by agent orchestration.

    Stores execution output,
    reasoning information and metadata.
    """


    status: str

    result: Any = None

    reasoning: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )



    def to_dict(
        self
    ) -> Dict[str, Any]:
        """
        Convert orchestration result
        into dictionary format.
        """

        return {

            "status": self.status,

            "result": self.result,

            "reasoning": self.reasoning,

            "metadata": self.metadata

        }