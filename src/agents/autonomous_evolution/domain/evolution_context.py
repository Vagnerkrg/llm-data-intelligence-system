from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class EvolutionContext:
    """
    Contains the information required to evaluate a potential evolution.

    The context intentionally accepts generic values so the evolution
    domain remains independent from runtime, memory, evaluation systems,
    improvement systems, and external providers.
    """

    execution_information: Any = None
    evaluation_information: Any = None
    learning_information: Any = None
    knowledge_information: Any = None
    memory_information: Any = None
    improvement_information: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the evolution context into a dictionary.
        """
        return asdict(self)