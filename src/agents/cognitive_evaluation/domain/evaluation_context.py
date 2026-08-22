from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class EvaluationContext:
    """
    Contains the information required to evaluate an agent execution.

    The context intentionally accepts generic values because the
    evaluation layer integrates information produced by different
    cognitive subsystems.
    """

    execution_result: Any = None
    reasoning_information: Any = None
    planning_information: Any = None
    memory_information: Any = None
    improvement_information: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the evaluation context into a dictionary.
        """
        return asdict(self)
