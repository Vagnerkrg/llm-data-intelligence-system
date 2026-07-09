from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ReasoningResult:
    """
    Represents the output produced
    by the reasoning engine.

    Stores the reasoning process,
    final conclusion and confidence.
    """


    reasoning: str

    conclusion: str

    confidence: float = 0.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )



    def to_dict(
        self
    ) -> Dict[str, Any]:
        """
        Convert reasoning result
        into dictionary format.
        """

        return {

            "reasoning": self.reasoning,

            "conclusion": self.conclusion,

            "confidence": self.confidence,

            "metadata": self.metadata

        }