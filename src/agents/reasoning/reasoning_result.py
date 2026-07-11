from dataclasses import dataclass, field
from typing import Any, Dict, List



@dataclass
class ReasoningResult:
    """
    Represents the output produced
    by the reasoning engine.

    Stores the reasoning process,
    final conclusion, confidence,
    and structured reasoning information
    used by planning layers.
    """


    reasoning: str

    conclusion: str

    confidence: float = 0.0


    goal: str = ""

    intent: str = ""


    required_capabilities: List[str] = field(
        default_factory=list
    )


    strategy: str = ""


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

            "goal": self.goal,

            "intent": self.intent,

            "required_capabilities": (
                self.required_capabilities
            ),

            "strategy": self.strategy,

            "metadata": self.metadata

        }
   
    