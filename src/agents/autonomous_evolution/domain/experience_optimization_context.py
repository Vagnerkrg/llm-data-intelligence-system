from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ExperienceOptimizationContext:
    """
    Represents the accumulated information used to derive
    experience-driven optimization signals.

    The domain remains independent from runtime implementations,
    memory providers, learning engines, and external systems.
    """

    execution_history: list[Any] = field(default_factory=list)
    cognitive_evaluations: list[Any] = field(default_factory=list)
    memory_information: Any = None
    learning_outcomes: list[Any] = field(default_factory=list)
    knowledge_information: Any = None
    evolution_decisions: list[Any] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the optimization context into a dictionary.
        """
        return asdict(self)